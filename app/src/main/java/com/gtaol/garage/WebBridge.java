package com.gtaol.garage;

import android.content.ContentValues;
import android.content.Context;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.webkit.JavascriptInterface;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/**
 * 原生桥：
 * - saveState / loadState  —— 数据持久化到 SharedPreferences，覆盖安装不丢
 * - saveBackup            —— 导出到「下载」目录
 * - webdavPut / webdavGet —— WebDAV 云备份（原生网络，绕开 WebView CORS）
 */
public class WebBridge {

    private final Context ctx;
    private static final String PREFS = "gtaol_garage";

    WebBridge(Context ctx) {
        this.ctx = ctx;
    }

    /* ---------- 数据持久化（升级保留） ---------- */

    @JavascriptInterface
    public String loadState() {
        SharedPreferences sp = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        return sp.getString("state", null);
    }

    @JavascriptInterface
    public void saveState(String json) {
        if (json == null || json.isEmpty()) return;
        SharedPreferences sp = ctx.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        sp.edit().putString("state", json).apply();
    }

    /* ---------- 导出到下载目录 ---------- */

    @JavascriptInterface
    public boolean saveBackup(String json, String filename) {
        if (json == null || json.isEmpty()) return false;
        if (filename == null || filename.isEmpty()) filename = "gtaol-vehicles-backup.json";

        try {
            byte[] bytes = json.getBytes(StandardCharsets.UTF_8);

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                ContentValues cv = new ContentValues();
                cv.put(MediaStore.MediaColumns.DISPLAY_NAME, filename);
                cv.put(MediaStore.MediaColumns.MIME_TYPE, "application/json");
                cv.put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS);
                Uri uri = ctx.getContentResolver().insert(
                        MediaStore.Downloads.EXTERNAL_CONTENT_URI, cv);
                if (uri == null) return false;
                try (OutputStream os = ctx.getContentResolver().openOutputStream(uri)) {
                    if (os == null) return false;
                    os.write(bytes);
                    os.flush();
                }
            } else {
                File dir = Environment.getExternalStoragePublicDirectory(
                        Environment.DIRECTORY_DOWNLOADS);
                if (!dir.exists() && !dir.mkdirs()) return false;
                File out = new File(dir, filename);
                try (FileOutputStream fos = new FileOutputStream(out)) {
                    fos.write(bytes);
                    fos.flush();
                }
            }

            notify("已保存到「下载」文件夹：" + filename);
            return true;

        } catch (Exception e) {
            notify("导出失败：" + e.getMessage());
            return false;
        }
    }

    /* ---------- WebDAV ---------- */

    @JavascriptInterface
    public String webdavPut(String url, String username, String password, String content) {
        return webdavRequest(url, username, password, "PUT", content);
    }

    @JavascriptInterface
    public String webdavGet(String url, String username, String password) {
        return webdavRequest(url, username, password, "GET", null);
    }

    private String webdavRequest(final String url,
                                 final String username,
                                 final String password,
                                 final String method,
                                 final String body) {
        if (url == null || url.isEmpty()) return "ERR:服务器地址为空";
        if (!url.startsWith("http://") && !url.startsWith("https://"))
            return "ERR:地址需以 http:// 或 https:// 开头";

        final CountDownLatch latch = new CountDownLatch(1);
        final AtomicReference<String> result = new AtomicReference<>(null);

        new Thread(new Runnable() {
            @Override public void run() {
                HttpURLConnection conn = null;
                try {
                    URL u = new URL(url);
                    conn = (HttpURLConnection) u.openConnection();
                    conn.setRequestMethod(method);
                    conn.setConnectTimeout(15000);
                    conn.setReadTimeout(30000);
                    conn.setDoInput(true);
                    conn.setRequestProperty("User-Agent", "GTAOL-Garage/1.0");

                    if (username != null && !username.isEmpty()) {
                        String raw = username + ":" + (password == null ? "" : password);
                        String auth = Base64.encodeToString(
                                raw.getBytes(StandardCharsets.UTF_8), Base64.NO_WRAP);
                        conn.setRequestProperty("Authorization", "Basic " + auth);
                    }

                    if ("PUT".equals(method)) {
                        conn.setDoOutput(true);
                        conn.setRequestProperty("Content-Type", "application/json; charset=utf-8");
                        byte[] b = (body == null ? "" : body).getBytes(StandardCharsets.UTF_8);
                        conn.setFixedLengthStreamingMode(b.length);
                        OutputStream os = conn.getOutputStream();
                        os.write(b);
                        os.flush();
                        os.close();
                    }

                    int code = conn.getResponseCode();
                    if (code >= 200 && code < 300) {
                        if ("GET".equals(method)) {
                            InputStream is = conn.getInputStream();
                            ByteArrayOutputStream bos = new ByteArrayOutputStream();
                            byte[] buf = new byte[8192];
                            int n;
                            while ((n = is.read(buf)) > 0) bos.write(buf, 0, n);
                            is.close();
                            result.set("OK:" + new String(bos.toByteArray(), StandardCharsets.UTF_8));
                        } else {
                            result.set("OK");
                        }
                    } else {
                        result.set("ERR:HTTP " + code);
                    }
                } catch (Exception e) {
                    result.set("ERR:" + e.getClass().getSimpleName());
                } finally {
                    if (conn != null) conn.disconnect();
                    latch.countDown();
                }
            }
        }).start();

        try {
            latch.await(35, TimeUnit.SECONDS);
        } catch (InterruptedException ignored) {}

        String r = result.get();
        return r == null ? "ERR:timeout" : r;
    }

    private void notify(final String msg) {
        if (ctx instanceof MainActivity) {
            ((MainActivity) ctx).toastOnUi(msg);
        }
    }
}
