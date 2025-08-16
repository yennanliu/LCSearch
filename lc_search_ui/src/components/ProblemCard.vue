<template>
  <div class="problem-card">
    <div class="problem-header">
      <div class="problem-title-section">
        <a 
          :href="problem.url" 
          target="_blank" 
          rel="noopener noreferrer"
          class="problem-title"
        >
          {{ problem.title }}
          <span class="external-link">↗</span>
        </a>
        <div class="problem-meta">
          <span :class="['difficulty', problem.difficulty.toLowerCase()]">
            {{ problem.difficulty }}
          </span>
          <span class="problem-id">#{{ problem.id }}</span>
          <span class="date-added">{{ formatDate(problem.dateAdded) }}</span>
        </div>
      </div>
    </div>

    <div v-if="problem.description" class="problem-description">
      {{ problem.description }}
    </div>

    <div class="problem-tags">
      <div class="tag-group">
        <span class="tag-label">Tags:</span>
        <div class="tags">
          <span 
            v-for="tag in problem.tags" 
            :key="tag"
            class="tag tag-type"
          >
            {{ tag }}
          </span>
        </div>
      </div>

      <div class="tag-group">
        <span class="tag-label">Patterns:</span>
        <div class="tags">
          <span 
            v-for="pattern in problem.patterns" 
            :key="pattern"
            class="tag tag-pattern"
          >
            {{ pattern }}
          </span>
        </div>
      </div>

      <div v-if="problem.companies.length > 0" class="tag-group">
        <span class="tag-label">Companies:</span>
        <div class="tags">
          <span 
            v-for="company in problem.companies.slice(0, 5)" 
            :key="company"
            class="tag tag-company"
          >
            {{ company }}
          </span>
          <span 
            v-if="problem.companies.length > 5"
            class="tag tag-company more-count"
          >
            +{{ problem.companies.length - 5 }} more
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProblemCard',
  props: {
    problem: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
  }
}
</script>

<style scoped>
.problem-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  transition: all 0.2s ease;
}

.problem-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #ddd;
}

.problem-header {
  margin-bottom: 1rem;
}

.problem-title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.problem-title {
  color: #1976d2;
  text-decoration: none;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s ease;
}

.problem-title:hover {
  color: #1565c0;
  text-decoration: underline;
}

.external-link {
  font-size: 0.8rem;
  opacity: 0.7;
}

.problem-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
}

.difficulty {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.difficulty.easy {
  background: #d4edda;
  color: #155724;
}

.difficulty.medium {
  background: #fff3cd;
  color: #856404;
}

.difficulty.hard {
  background: #f8d7da;
  color: #721c24;
}

.problem-id {
  color: #666;
  font-weight: 500;
}

.date-added {
  color: #666;
  font-size: 0.8rem;
}

.problem-description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.problem-tags {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tag-group {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.tag-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #333;
  min-width: 80px;
  padding-top: 2px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  flex: 1;
}

.tag {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.tag-type {
  background: #e3f2fd;
  color: #1976d2;
}

.tag-pattern {
  background: #f3e5f5;
  color: #7b1fa2;
}

.tag-company {
  background: #e8f5e8;
  color: #2e7d32;
}

.more-count {
  background: #f5f5f5;
  color: #666;
  font-style: italic;
}

@media (max-width: 768px) {
  .problem-card {
    padding: 1rem;
  }
  
  .problem-title {
    font-size: 1.1rem;
  }
  
  .problem-meta {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .tag-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
  
  .tag-label {
    min-width: auto;
  }
}
</style>