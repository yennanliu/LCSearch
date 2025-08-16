<template>
  <div class="problem-list">
    <div v-if="loading" class="loading">
      Loading problems...
    </div>
    
    <div v-else-if="problems.length === 0" class="no-results">
      <h3>No problems found</h3>
      <p>Try adjusting your search or filters</p>
    </div>
    
    <div v-else>
      <div class="results-header">
        <p class="results-count">
          {{ problems.length }} problem{{ problems.length !== 1 ? 's' : '' }} found
        </p>
        <div class="items-per-page">
          <label for="items-per-page">Show:</label>
          <select 
            id="items-per-page"
            v-model="itemsPerPage" 
            @change="handleItemsPerPageChange"
            class="items-select"
          >
            <option value="5">5 per page</option>
            <option value="10">10 per page</option>
            <option value="20">20 per page</option>
            <option value="50">50 per page</option>
          </select>
        </div>
      </div>

      <div class="problems-container">
        <ProblemCard
          v-for="problem in paginatedProblems"
          :key="problem.id"
          :problem="problem"
        />
      </div>

      <ProblemPagination
        :current-page="currentPage"
        :total-items="problems.length"
        :items-per-page="itemsPerPage"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import ProblemCard from './ProblemCard.vue'
import ProblemPagination from './Pagination.vue'

export default {
  name: 'ProblemList',
  components: {
    ProblemCard,
    ProblemPagination
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
  },
  setup(props) {
    const currentPage = ref(1)
    const itemsPerPage = ref(10)

    const paginatedProblems = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return props.problems.slice(start, end)
    })

    const handlePageChange = (page) => {
      currentPage.value = page
      // Scroll to top of results
      const problemList = document.querySelector('.problem-list')
      if (problemList) {
        problemList.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }

    const handleItemsPerPageChange = () => {
      currentPage.value = 1 // Reset to first page when changing items per page
    }

    // Reset to first page when problems change (new search/filter)
    watch(() => props.problems, () => {
      currentPage.value = 1
    })

    return {
      currentPage,
      itemsPerPage,
      paginatedProblems,
      handlePageChange,
      handleItemsPerPageChange
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.results-count {
  margin: 0;
  color: #374151;
  font-size: 1rem;
  font-weight: 600;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.items-per-page label {
  color: #6b7280;
  font-size: 0.9rem;
  font-weight: 500;
}

.items-select {
  padding: 8px 12px;
  border: 2px solid rgba(103, 126, 234, 0.2);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  color: #374151;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  transition: all 0.3s ease;
}

.items-select:focus,
.items-select:hover {
  border-color: rgba(103, 126, 234, 0.4);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 12px rgba(103, 126, 234, 0.1);
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
  
  .results-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
    text-align: center;
  }
  
  .items-per-page {
    justify-content: center;
  }
}
</style>