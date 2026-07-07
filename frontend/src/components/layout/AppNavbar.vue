<template>
  <header class="app-navbar" :class="{ 'is-workspace': workspace }">
    <div class="navbar-inner">
      <RouterLink class="brand" to="/" aria-label="LeetPrep-SQL dashboard">
        <span class="brand-mark">
          <img src="/favicon.png" alt="SQL logo" />
        </span>
        <span>LeetPrep-SQL</span>
      </RouterLink>

      <nav class="nav-links" aria-label="Primary navigation">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/roadmap">Roadmap</RouterLink>
        <RouterLink to="/problems">Problems</RouterLink>
      </nav>

      <button
        class="theme-toggle"
        type="button"
        :aria-label="`Switch to ${nextThemeLabel} mode`"
        :title="`Switch to ${nextThemeLabel} mode`"
        @click="toggleTheme"
      >
        <svg
          v-if="theme === 'dark'"
          aria-hidden="true"
          viewBox="0 0 24 24"
        >
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2v2" />
          <path d="M12 20v2" />
          <path d="m4.93 4.93 1.41 1.41" />
          <path d="m17.66 17.66 1.41 1.41" />
          <path d="M2 12h2" />
          <path d="M20 12h2" />
          <path d="m6.34 17.66-1.41 1.41" />
          <path d="m19.07 4.93-1.41 1.41" />
        </svg>
        <svg
          v-else
          aria-hidden="true"
          viewBox="0 0 24 24"
        >
          <path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5 7 7 0 1 0 20.5 14.5Z" />
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";

import { getStoredTheme, saveTheme } from "../../services/themeStorage";

defineProps({
  workspace: {
    type: Boolean,
    default: false,
  },
});

const theme = ref(getStoredTheme());
const nextThemeLabel = ref(theme.value === "dark" ? "light" : "dark");

function toggleTheme() {
  theme.value = theme.value === "dark" ? "light" : "dark";
  nextThemeLabel.value = theme.value === "dark" ? "light" : "dark";
  saveTheme(theme.value);
}
</script>

<style scoped>
.app-navbar {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-nav-bg);
  backdrop-filter: blur(12px);
  min-height: 45px;
  padding: 6px 0;
}

.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: var(--space-3);
  width: min(1280px, calc(100% - 24px));
  margin: 0 auto;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text);
  font-size: 15px;
  font-weight: 850;
  white-space: nowrap;
}

.brand-mark {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: none;
  padding: 0;
}

.brand-mark img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.nav-links {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: var(--space-1);
  margin-left: auto;
}

.nav-links a {
  border-radius: var(--radius-sm);
  color: var(--color-muted);
  font-size: var(--font-sm);
  font-weight: 750;
  padding: 6px 9px;
}

.nav-links a.router-link-active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.app-navbar.is-workspace {
  border-bottom-color: var(--color-border);
  background: var(--color-nav-bg);
}

.app-navbar.is-workspace .brand {
  color: var(--color-text);
}

.app-navbar.is-workspace .brand-mark {
  background: var(--color-primary);
  color: #ffffff;
}

.app-navbar.is-workspace .nav-links a {
  color: var(--color-text-muted);
}

.app-navbar.is-workspace .nav-links a.router-link-active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.theme-toggle {
  display: inline-grid;
  place-items: center;
  width: 32px;
  min-height: 30px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface-muted);
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0;
}

.theme-toggle:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.theme-toggle svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2;
}

@media (max-width: 560px) {
  .navbar-inner {
    align-items: flex-start;
    flex-direction: column;
    width: min(100% - 16px, 1280px);
  }

  .nav-links {
    justify-content: flex-start;
    margin-left: 0;
    width: 100%;
  }
}
</style>
