<template>
  <div class="filter-panel">
    <div class="filter-section">
      <label class="filter-label">Difficulty:</label>
      <select v-model="selectedDifficulty" @change="updateFilters" class="filter-select">
        <option value="">All Difficulties</option>
        <option value="Easy">Easy</option>
        <option value="Medium">Medium</option>
        <option value="Hard">Hard</option>
      </select>
    </div>

    <div class="filter-section">
      <label class="filter-label">Tags:</label>
      <div class="filter-chips">
        <button
          v-for="tag in allTags.slice(0, showAllTags ? allTags.length : 8)"
          :key="tag"
          :class="['filter-chip', { active: selectedTags.includes(tag) }]"
          @click="toggleTag(tag)"
        >
          {{ tag }}
        </button>
        <button 
          v-if="allTags.length > 8"
          @click="showAllTags = !showAllTags"
          class="show-more-btn"
        >
          {{ showAllTags ? 'Show Less' : `Show ${allTags.length - 8} More` }}
        </button>
      </div>
    </div>

    <div class="filter-section">
      <label class="filter-label">Patterns:</label>
      <div class="filter-chips">
        <button
          v-for="pattern in allPatterns.slice(0, showAllPatterns ? allPatterns.length : 8)"
          :key="pattern"
          :class="['filter-chip', { active: selectedPatterns.includes(pattern) }]"
          @click="togglePattern(pattern)"
        >
          {{ pattern }}
        </button>
        <button 
          v-if="allPatterns.length > 8"
          @click="showAllPatterns = !showAllPatterns"
          class="show-more-btn"
        >
          {{ showAllPatterns ? 'Show Less' : `Show ${allPatterns.length - 8} More` }}
        </button>
      </div>
    </div>

    <div class="filter-section">
      <label class="filter-label">Companies:</label>
      <div class="filter-chips">
        <button
          v-for="company in allCompanies.slice(0, showAllCompanies ? allCompanies.length : 8)"
          :key="company"
          :class="['filter-chip', { active: selectedCompanies.includes(company) }]"
          @click="toggleCompany(company)"
        >
          {{ company }}
        </button>
        <button 
          v-if="allCompanies.length > 8"
          @click="showAllCompanies = !showAllCompanies"
          class="show-more-btn"
        >
          {{ showAllCompanies ? 'Show Less' : `Show ${allCompanies.length - 8} More` }}
        </button>
      </div>
    </div>

    <div v-if="hasActiveFilters" class="filter-actions">
      <button @click="clearAllFilters" class="clear-filters-btn">
        Clear All Filters
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'FilterPanel',
  props: {
    allTags: {
      type: Array,
      required: true
    },
    allPatterns: {
      type: Array,
      required: true
    },
    allCompanies: {
      type: Array,
      required: true
    }
  },
  emits: ['filter'],
  setup(props, { emit }) {
    const selectedDifficulty = ref('')
    const selectedTags = ref([])
    const selectedPatterns = ref([])
    const selectedCompanies = ref([])
    
    const showAllTags = ref(false)
    const showAllPatterns = ref(false)
    const showAllCompanies = ref(false)

    const hasActiveFilters = computed(() => {
      return selectedDifficulty.value ||
             selectedTags.value.length > 0 ||
             selectedPatterns.value.length > 0 ||
             selectedCompanies.value.length > 0
    })

    const toggleTag = (tag) => {
      const index = selectedTags.value.indexOf(tag)
      if (index > -1) {
        selectedTags.value.splice(index, 1)
      } else {
        selectedTags.value.push(tag)
      }
      updateFilters()
    }

    const togglePattern = (pattern) => {
      const index = selectedPatterns.value.indexOf(pattern)
      if (index > -1) {
        selectedPatterns.value.splice(index, 1)
      } else {
        selectedPatterns.value.push(pattern)
      }
      updateFilters()
    }

    const toggleCompany = (company) => {
      const index = selectedCompanies.value.indexOf(company)
      if (index > -1) {
        selectedCompanies.value.splice(index, 1)
      } else {
        selectedCompanies.value.push(company)
      }
      updateFilters()
    }

    const updateFilters = () => {
      emit('filter', {
        difficulty: selectedDifficulty.value,
        tags: [...selectedTags.value],
        patterns: [...selectedPatterns.value],
        companies: [...selectedCompanies.value]
      })
    }

    const clearAllFilters = () => {
      selectedDifficulty.value = ''
      selectedTags.value = []
      selectedPatterns.value = []
      selectedCompanies.value = []
      updateFilters()
    }

    return {
      selectedDifficulty,
      selectedTags,
      selectedPatterns,
      selectedCompanies,
      showAllTags,
      showAllPatterns,
      showAllCompanies,
      hasActiveFilters,
      toggleTag,
      togglePattern,
      toggleCompany,
      updateFilters,
      clearAllFilters
    }
  }
}
</script>

<style scoped>
.filter-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  max-width: 200px;
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.filter-chip {
  padding: 6px 12px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-chip:hover {
  background: #e9ecef;
  border-color: #bbb;
}

.filter-chip.active {
  background: #1976d2;
  color: white;
  border-color: #1976d2;
}

.show-more-btn {
  padding: 6px 12px;
  background: none;
  border: 1px dashed #bbb;
  border-radius: 20px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.show-more-btn:hover {
  border-color: #1976d2;
  color: #1976d2;
}

.filter-actions {
  padding-top: 0.5rem;
  border-top: 1px solid #eee;
}

.clear-filters-btn {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.clear-filters-btn:hover {
  background: #c82333;
}

@media (max-width: 768px) {
  .filter-section {
    gap: 0.75rem;
  }
  
  .filter-chip {
    font-size: 12px;
    padding: 5px 10px;
  }
}
</style>