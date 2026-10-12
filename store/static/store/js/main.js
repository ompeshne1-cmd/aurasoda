/**
 * HERITAGE BREW - Interactive Client Logic
 * Handles Ajax Cart Additions, Live Pack Size Price Calculations,
 * Micro-animations, Quantity Steppers, and Toast Feedback.
 */

document.addEventListener('DOMContentLoaded', () => {
  initPackSelector();
  initQuantityControls();
  initAjaxAddToCart();
  initDetailTabs();
  initToasts();
  initMobileNav();
});

/* -------------------------------------------------------------
 * 1. Pack Selector on Product Detail Page
 * ----------------------------------------------------------- */
function initPackSelector() {
  const packCards = document.querySelectorAll('.pack-option-card');
  const priceDisplay = document.querySelector('.current-price');
  const packInput = document.getElementById('selected-pack-input');
  const unitLabel = document.querySelector('.price-unit-label');

  if (!packCards.length || !priceDisplay || !packInput) return;

  packCards.forEach(card => {
    card.addEventListener('click', () => {
      // Remove active class from all
      packCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');

      const packType = card.dataset.pack;
      const price = card.dataset.price;
      const label = card.dataset.label;

      packInput.value = packType;

      // Smooth number animation / update
      priceDisplay.textContent = `$${parseFloat(price).toFixed(2)}`;
      if (unitLabel) {
        unitLabel.textContent = `per ${label}`;
      }
    });
  });
}

/* -------------------------------------------------------------
 * 2. Quantity Increment / Decrement Controls
 * ----------------------------------------------------------- */
function initQuantityControls() {
  document.querySelectorAll('.quantity-control').forEach(wrap => {
    const minusBtn = wrap.querySelector('.qty-minus');
    const plusBtn = wrap.querySelector('.qty-plus');
    const input = wrap.querySelector('.qty-input');

    if (!input) return;

    if (minusBtn) {
      minusBtn.addEventListener('click', () => {
        let current = parseInt(input.value) || 1;
        if (current > 1) {
          input.value = current - 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    }

    if (plusBtn) {
      plusBtn.addEventListener('click', () => {
        let current = parseInt(input.value) || 1;
        input.value = current + 1;
        input.dispatchEvent(new Event('change'));
      });
    }
  });
}

/* -------------------------------------------------------------
 * 3. Ajax Add to Cart (Quick add on cards + Detail page)
 * ----------------------------------------------------------- */
function initAjaxAddToCart() {
  // Quick Add Buttons on Catalog Cards
  document.querySelectorAll('.ajax-add-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const productId = btn.dataset.productId;
      const csrfToken = getCsrfToken();

      const originalHtml = btn.innerHTML;
      btn.innerHTML = '⋯';
      btn.disabled = true;

      const formData = new FormData();
      formData.append('pack', 'single');
      formData.append('quantity', '1');

      try {
        const response = await fetch(`/cart/add/${productId}/`, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
          },
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          updateNavbarCartCount(data.cart_count);
          showToast(data.message || 'Added to your crate!', 'success');
        } else {
          // If fallback needed
          window.location.reload();
        }
      } catch (err) {
        console.error('Add to cart error:', err);
      } finally {
        btn.innerHTML = originalHtml;
        btn.disabled = false;
      }
    });
  });

  // Main Form Add to Cart on Detail Page
  const detailForm = document.getElementById('add-to-crate-form');
  if (detailForm) {
    detailForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = detailForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'Adding to Crate...';
      submitBtn.disabled = true;

      const actionUrl = detailForm.action;
      const formData = new FormData(detailForm);
      const csrfToken = getCsrfToken();

      try {
        const response = await fetch(actionUrl, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
          },
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          updateNavbarCartCount(data.cart_count);
          showToast(data.message || 'Craft soda added to crate!', 'success');
        } else {
          detailForm.submit();
        }
      } catch (err) {
        detailForm.submit();
      } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    });
  }
}

function updateNavbarCartCount(count) {
  const badges = document.querySelectorAll('.crate-badge');
  badges.forEach(b => {
    b.textContent = count;
    b.style.transform = 'scale(1.25)';
    setTimeout(() => {
      b.style.transform = 'scale(1)';
    }, 250);
  });
}

/* -------------------------------------------------------------
 * 4. Detail Page Tabs
 * ----------------------------------------------------------- */
function initDetailTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  if (!tabBtns.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.style.display = 'none');

      btn.classList.add('active');
      const targetId = btn.dataset.target;
      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.style.display = 'block';
      }
    });
  });
}

/* -------------------------------------------------------------
 * 5. Toast Notifications
 * ----------------------------------------------------------- */
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast-item ${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentElement) {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }
  }, 4000);
}

function initToasts() {
  document.querySelectorAll('.toast-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.parentElement.remove();
    });
  });
}

/* -------------------------------------------------------------
 * 6. Mobile Navigation
 * ----------------------------------------------------------- */
function initMobileNav() {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.nav-links');

  if (!toggle || !nav) return;

  toggle.addEventListener('click', () => {
    if (nav.style.display === 'flex') {
      nav.style.display = 'none';
    } else {
      nav.style.display = 'flex';
      nav.style.flexDirection = 'column';
      nav.style.position = 'absolute';
      nav.style.top = '100%';
      nav.style.left = '0';
      nav.style.width = '100%';
      nav.style.background = 'var(--bg-card)';
      nav.style.padding = '1.5rem';
      nav.style.borderBottom = '1px solid var(--border-subtle)';
    }
  });
}

/* Helper to get CSRF token */
function getCsrfToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}
