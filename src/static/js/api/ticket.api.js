/**
 * src/static/js/api/ticket.api.js
 * ─── Nghiệp vụ API Luồng L02 ───
 * Tất cả gọi API đi qua client.js - không gọi fetch() trực tiếp.
 */

import { apiGet, apiPost } from "./client.js";

/** Tra cứu khách hàng theo SĐT (QT-01, QT-02, QT-15). */
export const searchCustomer = (phone) =>
  apiPost("/customers/search", { phone });

/** Khởi tạo phiếu bảo hành mới (QT-03 → QT-06). */
export const createTicket = (payload) =>
  apiPost("/tickets", payload);

/** Lấy danh sách phiếu với bộ lọc (US7). */
export const getTickets = ({ status, overdue_only, keyword } = {}) =>
  apiGet("/tickets", { status, overdue_only, keyword });

/** Chi tiết phiếu kèm log trạng thái (M3). */
export const getTicketDetail = (ticketCode) =>
  apiGet(`/tickets/${ticketCode}`);

/** Danh sách nhóm sự cố từ CSDL. */
export const getCategories = () =>
  apiGet("/categories");
