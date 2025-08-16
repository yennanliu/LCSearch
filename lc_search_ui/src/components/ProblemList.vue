<template>
  <div class="problem-list">
    <div v-if="loading" class="loading">
      Loading problems...
    </div>
    
    <div v-else-if="problems.length === 0" class="no-results">
      <h3>No problems found</h3>
      <p>Try adjusting your search or filters</p>
    </div>
    
    <div v-else class="results-header">
      <p class="results-count">
        {{ problems.length }} problem{{ problems.length !== 1 ? 's' : '' }} found
      </p>
    </div>

    <div class="problems-container">
      <ProblemCard
        v-for="problem in problems"
        :key="problem.id"
        :problem="problem"
      />
    </div>
  </div>
</template>

<script>
import ProblemCard from './ProblemCard.vue'

export default {
  name: 'ProblemList',
  components: {
    ProblemCard
  },
  props: {
    problems: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.problem-list {
  width: 100%;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #666;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.no-results h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.no-results p {
  margin: 0;
  font-size: 0.9rem;
}

.results-header {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.results-count {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.problems-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (max-width: 768px) {
  .problems-container {
    gap: 0.75rem;
  }
}
</style>