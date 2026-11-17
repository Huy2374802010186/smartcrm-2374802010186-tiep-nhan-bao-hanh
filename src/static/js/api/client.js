/**
 * src/static/js/api/client.js
 * ─── Tầng API Client duy nhất (Track SE - Luồng L02) ───
 * Toàn bộ giao tiếp HTTP đi qua module này.
 * Tuyệt đối KHÔNG gọi fetch() trực tiếp từ pages/components.
 */

const BASE_URL = "http://localhost:8000/api/v1";

/**
 * Hàm gọi API cơ sở - xử lý lỗi mạng tập trung.
 * @param {string} path  - đường dẫn tương đối, vd: "/tickets"
 * @param {object} opts  - RequestInit options
 * @returns {Promise<any>} - JSON đã parse
 */
async function _request(path, opts = {}) {
  const url = `${BASE_URL}${path}`;
  const defaultHeaders = { "Content-Type": "application/json" };

  let response;
  try {
    response = await fetch(url, {
      ...opts,
      headers: { ...defaultHeaders, ...(opts.headers || {}) },
    });
  } catch (networkErr) {
    // Lỗi mất kết nối (server tắt hoặc không có mạng)
    throw new Error("NETWORK_ERROR: Không thể kết nối tới Backend. Vui lòng kiểm tra server đang chạy.");
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const msg = data?.message || `HTTP ${response.status}: ${response.statusText}`;
    const err = new Error(msg);
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}

/** GET /v1 */
export const apiGet = (path, params = {}) => {
  const qs = new URLSearchParams(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "")
  ).toString();
  return _request(`${path}${qs ? "?" + qs : ""}`);
};

/** POST /v1 */
export const apiPost = (path, body) =>
  _request(path, { method: "POST", body: JSON.stringify(body) });
