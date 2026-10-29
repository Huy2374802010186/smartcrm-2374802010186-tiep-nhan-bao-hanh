/**
 * src/static/js/app.js
 * ─── Controller chính cho 3 màn hình M1, M2, M3 ───
 * Tất cả gọi API đi qua ticket.api.js (không fetch trực tiếp).
 */

import { searchCustomer, createTicket, getTickets, getTicketDetail, getCategories } from "./api/ticket.api.js";

// ────────────────────────────────────────────────────────────
// UTILS
// ────────────────────────────────────────────────────────────

/** Hiển thị component DataState (loading / empty / error) */
function showDataState(containerId, type, { title, sub, retryFn } = {}) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.classList.remove("hidden");

  if (type === "loading") {
    el.innerHTML = `<div class="spinner"></div><div class="ds-title">Đang tải dữ liệu...</div>`;
  } else if (type === "empty") {
    el.innerHTML = `<div class="ds-icon">📭</div><div class="ds-title">${title || "Không có kết quả"}</div><div class="ds-sub">${sub || "Thử thay đổi bộ lọc hoặc tạo phiếu mới"}</div>`;
  } else if (type === "error") {
    const btnHtml = retryFn
      ? `<button class="btn-primary" style="margin-top:8px" onclick="(${retryFn.toString()})()">🔄 Thử lại</button>`
      : "";
    el.innerHTML = `<div class="ds-icon">⚠️</div><div class="ds-title" style="color:var(--clr-danger)">${title || "Đã xảy ra lỗi"}</div><div class="ds-sub">${sub || ""}</div>${btnHtml}`;
  }
}

function hideDataState(containerId) {
  const el = document.getElementById(containerId);
  if (el) el.classList.add("hidden");
}

function formatDate(isoStr) {
  if (!isoStr) return "—";
  try {
    return new Date(isoStr).toLocaleString("vi-VN", { dateStyle: "short", timeStyle: "short" });
  } catch { return isoStr; }
}

/** Tính SLA due_date phía client (bỏ qua Chủ Nhật – QT-04) */
function calcSLA(priority) {
  const hours = { CAO: 24, TRUNG_BINH: 72, THAP: 120 }[priority] || 72;
  let cur = new Date();
  let added = 0;
  while (added < hours) {
    cur = new Date(cur.getTime() + 3600000); // +1h
    if (cur.getDay() !== 0) added++; // bỏ qua Chủ Nhật (0)
  }
  return cur;
}

/** Kiểm tra bảo hành 12 tháng (QT-05) */
function checkWarranty(purchaseDateStr) {
  if (!purchaseDateStr) return null;
  const purchase = new Date(purchaseDateStr);
  const today = new Date();
  const months = (today.getFullYear() - purchase.getFullYear()) * 12 + (today.getMonth() - purchase.getMonth());
  return months <= 12;
}

// ────────────────────────────────────────────────────────────
// NAVIGATION
// ────────────────────────────────────────────────────────────

window.showPage = function (pageId, navEl) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach(n => n.classList.remove("active"));
  document.getElementById(`page-${pageId}`)?.classList.add("active");
  if (navEl) navEl.classList.add("active");
  if (pageId === "m2") loadTickets();
};

// ────────────────────────────────────────────────────────────
// M1 — TIẾP NHẬN & TẠO PHIẾU
// ────────────────────────────────────────────────────────────

// ── Tải danh mục sự cố khi khởi động ──
async function loadCategories() {
  try {
    const res = await getCategories();
    const sel = document.getElementById("inp-category");
    sel.innerHTML = `<option value="">-- Chọn nhóm sự cố --</option>`;
    (res.data || []).forEach(c => {
      sel.innerHTML += `<option value="${c.category_id}" data-priority="${c.default_priority}">${c.category_name} — ${c.description?.slice(0, 30)}...</option>`;
    });
  } catch {
    document.getElementById("inp-category").innerHTML = `<option value="">Lỗi tải danh mục</option>`;
  }
}

window.onCategoryChange = function () {
  const sel = document.getElementById("inp-category");
  const opt = sel.options[sel.selectedIndex];
  const prio = opt?.dataset?.priority;
  if (prio) {
    const radio = document.querySelector(`input[name="priority"][value="${prio}"]`);
    if (radio) { radio.checked = true; }
  }
  updateSLA();
};

window.updateSLA = function () {
  const priority = document.querySelector('input[name="priority"]:checked')?.value;
  if (!priority) return;
  const due = calcSLA(priority);
  const slaEl = document.getElementById("sla-display");
  const slaText = document.getElementById("sla-text");
  slaEl.classList.remove("hidden");
  slaText.textContent = `Hạn cam kết trả máy (SLA): ${formatDate(due.toISOString())} (bỏ qua CN – QT-04)`;
};

// Theo dõi số ký tự mô tả
document.getElementById("inp-desc")?.addEventListener("input", function () {
  const n = this.value.length;
  const counter = document.getElementById("desc-counter");
  counter.textContent = `${n} ký tự ${n < 10 ? `(cần thêm ${10 - n})` : "✓ Hợp lệ"}`;
  counter.className = `char-counter ${n >= 10 ? "valid" : "invalid"}`;
});

// Theo dõi ngày mua để cập nhật bảo hành
document.getElementById("inp-purchase")?.addEventListener("change", function () {
  const badge = document.getElementById("warranty-status");
  if (!this.value) { badge.classList.add("hidden"); return; }
  const valid = checkWarranty(this.value);
  badge.classList.remove("hidden", "valid", "invalid");
  badge.classList.add(valid ? "valid" : "invalid");
  badge.textContent = valid ? "✓ CÒN BẢO HÀNH (QT-05)" : "✗ HẾT HẠN BẢO HÀNH (QT-05)";
});

// ── Tra cứu khách hàng ──
window.handleSearchCustomer = async function () {
  const phone = document.getElementById("inp-phone").value.trim();
  if (!phone) { alert("Vui lòng nhập số điện thoại."); return; }

  const dsEl = document.getElementById("ds-customer");
  const infoEl = document.getElementById("customer-info");
  infoEl.classList.add("hidden");
  dsEl.classList.remove("hidden");
  showDataState("ds-customer", "loading");

  try {
    const res = await searchCustomer(phone);
    hideDataState("ds-customer");
    const d = res.data;
    document.getElementById("cust-name").textContent = d.full_name || "—";
    document.getElementById("cust-phone").textContent = d.phone_normalized || "—";
    document.getElementById("cust-phone-masked").textContent = d.phone_masked || "—";
    document.getElementById("cust-email").textContent = d.email || "—";
    infoEl.classList.remove("hidden");
  } catch (err) {
    if (err.status === 404) {
      showDataState("ds-customer", "empty", { title: "Không tìm thấy khách hàng", sub: "SĐT chưa có trong hệ thống. Bạn có thể tiếp tục nhập thông tin thiết bị để tạo phiếu." });
    } else {
      showDataState("ds-customer", "error", {
        title: "Lỗi kết nối",
        sub: err.message,
        retryFn: window.handleSearchCustomer
      });
    }
  }
};

// ── Tạo phiếu bảo hành ──
window.handleCreateTicket = async function () {
  const phone = document.getElementById("inp-phone").value.trim();
  const serial = document.getElementById("inp-serial").value.trim();
  const purchase = document.getElementById("inp-purchase").value;
  const catId = parseInt(document.getElementById("inp-category").value);
  const desc = document.getElementById("inp-desc").value.trim();
  const priority = document.querySelector('input[name="priority"]:checked')?.value;

  // Validate
  if (!phone)    { alert("Vui lòng nhập số điện thoại."); return; }
  if (!serial)   { alert("Vui lòng nhập số Serial/IMEI."); return; }
  if (!catId)    { alert("Vui lòng chọn nhóm sự cố."); return; }
  if (desc.length < 10) { alert("Mô tả lỗi phải có ít nhất 10 ký tự (V8)."); return; }
  if (!priority) { alert("Vui lòng chọn mức ưu tiên."); return; }

  const btn = document.getElementById("btn-create");
  btn.disabled = true;
  btn.textContent = "Đang tạo phiếu...";

  try {
    const payload = { customer_phone: phone, serial_no: serial, category_id: catId, issue_desc: desc, priority };
    if (purchase) payload.purchase_date = purchase;

    const res = await createTicket(payload);
    const t = res.data;

    // Hiển thị modal thành công
    document.getElementById("modal-ticket-code").textContent = t.ticket_code;
    document.getElementById("modal-sla").textContent = `🕐 Hạn SLA: ${formatDate(t.due_date)}`;
    document.getElementById("modal-warranty").textContent = t.is_warranty ? "✅ Còn bảo hành" : "⚠️ Hết hạn bảo hành";
    document.getElementById("modal-success").classList.remove("hidden");
  } catch (err) {
    if (err.status === 409) {
      alert(`⚠️ ${err.message}`);
    } else {
      alert(`Lỗi: ${err.message}`);
    }
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>Tạo phiếu bảo hành`;
  }
};

window.closeModal = () => document.getElementById("modal-success").classList.add("hidden");

window.resetForm = function () {
  document.getElementById("form-ticket").reset();
  document.getElementById("customer-info").classList.add("hidden");
  document.getElementById("warranty-status").classList.add("hidden");
  document.getElementById("sla-display").classList.add("hidden");
  document.getElementById("ds-customer").classList.add("hidden");
  document.getElementById("desc-counter").textContent = "0 / tối thiểu 10 ký tự";
  document.getElementById("desc-counter").className = "char-counter";
};

// ────────────────────────────────────────────────────────────
// M2 — DANH SÁCH PHIẾU
// ────────────────────────────────────────────────────────────

async function loadTickets(params = {}) {
  const table = document.getElementById("ticket-table");
  const ds = document.getElementById("ds-tickets");
  table.classList.add("hidden");
  showDataState("ds-tickets", "loading");

  try {
    const res = await getTickets(params);
    hideDataState("ds-tickets");
    const tickets = res.data || [];

    if (tickets.length === 0) {
      showDataState("ds-tickets", "empty", { title: "Không tìm thấy phiếu", sub: "Thử thay đổi bộ lọc hoặc tạo phiếu mới" });
      return;
    }

    const tbody = document.getElementById("ticket-tbody");
    tbody.innerHTML = "";

    tickets.forEach(t => {
      const rowClass = t.is_overdue ? "row-overdue" : t.warning_sla ? "row-warning" : "";
      const slaLabel = t.is_overdue
        ? `<span style="color:var(--clr-danger)">🚨 Quá hạn</span>`
        : t.warning_sla
          ? `<span style="color:var(--clr-warning)">⚠️ Sắp hạn</span>`
          : "";

      const prioClass = { CAO: "p-cao", TRUNG_BINH: "p-tb", THAP: "p-thap" }[t.priority] || "";
      const prioLabel = { CAO: "CAO", TRUNG_BINH: "TB", THAP: "THẤP" }[t.priority] || t.priority;

      tbody.innerHTML += `
        <tr class="${rowClass}">
          <td><code style="color:var(--clr-accent);font-size:12px">${t.ticket_code}</code></td>
          <td>${t.customer_name || "—"}</td>
          <td><code style="color:var(--clr-accent);font-size:12px">${t.customer_phone_masked || "—"}</code></td>
          <td>${t.category_name || `#${t.category_id}`}</td>
          <td><span class="priority-pill ${prioClass}">${prioLabel}</span></td>
          <td><span class="status-badge status-${t.status}">${t.status?.replace(/_/g, " ")}</span></td>
          <td>${formatDate(t.due_date)} ${slaLabel}</td>
          <td>
            <button class="btn-link-sm" onclick="openTicketDetail('${t.ticket_code}')">Xem →</button>
          </td>
        </tr>`;
    });

    table.classList.remove("hidden");
  } catch (err) {
    showDataState("ds-tickets", "error", {
      title: "Lỗi tải danh sách",
      sub: err.message,
      retryFn: () => handleTicketFilter()
    });
  }
}

window.handleTicketFilter = function () {
  const status    = document.getElementById("f-status").value;
  const keyword   = document.getElementById("f-keyword").value.trim();
  const overdue   = document.getElementById("f-overdue").checked;
  loadTickets({ status: status || undefined, keyword: keyword || undefined, overdue_only: overdue || undefined });
};

// ────────────────────────────────────────────────────────────
// M3 — CHI TIẾT PHIẾU
// ────────────────────────────────────────────────────────────

window.openTicketDetail = async function (ticketCode) {
  document.getElementById("nav-m3").style.display = "flex";
  showPage("m3", document.getElementById("nav-m3"));
  document.getElementById("m3-title").textContent = `Chi tiết: ${ticketCode}`;
  document.getElementById("m3-content").classList.add("hidden");
  showDataState("ds-detail", "loading");

  try {
    const res = await getTicketDetail(ticketCode);
    hideDataState("ds-detail");
    const t = res.data;

    // Fill dữ liệu
    document.getElementById("d-code").textContent = t.ticket_code;
    const statusBadge = document.getElementById("d-status-badge");
    statusBadge.textContent = t.status?.replace(/_/g, " ");
    statusBadge.className = `status-badge status-${t.status}`;
    document.getElementById("d-cust-name").textContent   = t.customer_name || "—";
    document.getElementById("d-cust-phone").textContent  = t.customer_phone_masked || "—";
    document.getElementById("d-serial").textContent      = t.serial_no || "—";
    document.getElementById("d-category").textContent    = t.category_name || `#${t.category_id}`;
    document.getElementById("d-priority").textContent    = t.priority || "—";
    document.getElementById("d-warranty").textContent    = t.is_warranty ? "✅ Còn bảo hành" : "❌ Hết hạn";
    document.getElementById("d-due").textContent         = formatDate(t.due_date);
    document.getElementById("d-created").textContent     = formatDate(t.created_at);
    document.getElementById("d-desc").textContent        = t.issue_desc || "—";

    // Timeline
    const tl = document.getElementById("status-timeline");
    tl.innerHTML = "";
    (t.status_log || []).forEach(log => {
      const dotClass = {
        MOI: "dot-moi", DANG_XU_LY: "dot-dang", HOAN_TAT: "dot-hoan", DA_DONG: "dot-dong"
      }[log.to_status] || "dot-dong";

      tl.innerHTML += `
        <li class="timeline-item">
          <span class="timeline-dot ${dotClass}"></span>
          <div class="timeline-body">
            <div class="tl-status">${log.from_status ? `${log.from_status} → ` : ""}${log.to_status}</div>
            <div class="tl-meta">🕐 ${formatDate(log.changed_at)} &nbsp;|&nbsp; 👤 ${log.changed_by}</div>
            ${log.note ? `<div class="tl-note">${log.note}</div>` : ""}
          </div>
        </li>`;
    });

    document.getElementById("m3-content").classList.remove("hidden");
  } catch (err) {
    showDataState("ds-detail", "error", {
      title: "Không tải được phiếu",
      sub: err.message,
      retryFn: () => openTicketDetail(ticketCode)
    });
  }
};

// ────────────────────────────────────────────────────────────
// INIT
// ────────────────────────────────────────────────────────────
loadCategories();
updateSLA();
