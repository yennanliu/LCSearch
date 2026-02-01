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
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2rem;
  border: 2px solid rgba(255, 255, 255, 0.8);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06), 0 3px 10px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 56, 92, 0.04);
  position: relative;
  overflow: hidden;
}

.problem-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.7s;
}

.problem-card:hover::before {
  left: 100%;
}

.problem-card:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12), 0 12px 24px rgba(0, 0, 0, 0.08), 0 0 0 2px rgba(255, 56, 92, 0.12);
  border-color: rgba(255, 56, 92, 0.3);
  transform: translateY(-6px);
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
  color: #FF385C;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.3;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
}

.problem-title:hover {
  color: #FF6B98;
  text-decoration: none;
  transform: translateY(-1px);
}

.external-link {
  font-size: 0.8rem;
  opacity: 0.7;
}

.problem-meta {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: 0.95rem;
}

.difficulty {
  padding: 10px 20px;
  border-radius: 22px;
  font-weight: 700;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.difficulty.easy {
  background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.difficulty.medium {
  background: linear-gradient(135deg, #FFA726 0%, #FF9800 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.difficulty.hard {
  background: linear-gradient(135deg, #FF7043 0%, #FF5722 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.problem-id {
  color: #6b7280;
  font-weight: 600;
  font-size: 0.95rem;
}

.date-added {
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 500;
}

.problem-description {
  color: #374151;
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.problem-tags {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tag-group {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.tag-label {
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
  min-width: 90px;
  padding-top: 4px;
  letter-spacing: 0.02em;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  flex: 1;
}

.tag {
  padding: 6px 12px;
  border-radius: 14px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.01em;
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

  .problem-description {
    font-size: 1rem;
    line-height: 1.7;
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