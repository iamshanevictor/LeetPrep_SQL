<template>
  <section class="page">
    <RouterLink class="back-link" to="/problems">Back to Problems</RouterLink>
    <PageHeader
      eyebrow="Problem workspace"
      title="Problem Details"
      subtitle="Standalone problem details will appear here once practice problems are added."
    />

    <EmptyState
      title="This problem is not available yet."
      message="The app is currently focused on roadmap lessons and boss problems. Standalone problem content can be added later."
      action-label="Open Roadmap"
      action-to="/roadmap"
    />
  </section>
</template>

<script setup>
import PageHeader from "../components/layout/PageHeader.vue";
import EmptyState from "../components/ui/EmptyState.vue";
</script>
