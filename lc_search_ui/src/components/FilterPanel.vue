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
  gap: 1.5rem;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  color: #222222;
  font-size: 1.2rem;
  text-shadow: none;
  margin-bottom: 0.75rem;
}

.filter-select {
  padding: 16px 20px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 56, 92, 0.06);
  max-width: 260px;
  cursor: pointer;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #222222;
}

.filter-select:focus,
.filter-select:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12), 0 0 0 3px rgba(255, 56, 92, 0.15);
  transform: translateY(-2px);
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-chip {
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.98);
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 32px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  color: #222222;
  backdrop-filter: blur(20px);
  text-shadow: none;
  position: relative;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 0 0 1px rgba(255, 56, 92, 0.06);
}

.filter-chip::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.filter-chip:hover::before {
  left: 100%;
}

.filter-chip:hover {
  background: rgba(255, 255, 255, 1);
  border-color: rgba(255, 56, 92, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 1), 0 0 0 1px rgba(255, 56, 92, 0.1);
  color: #222222;
}

.filter-chip.active {
  background: linear-gradient(135deg, #FF385C 0%, #FF6B98 100%);
  border-color: #FF385C;
  color: white;
  font-weight: 800;
  box-shadow: 0 12px 30px rgba(255, 56, 92, 0.4), 0 6px 15px rgba(255, 56, 92, 0.25);
  transform: translateY(-4px);
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.filter-chip.active:hover {
  background: linear-gradient(135deg, #FF6B98 0%, #FFA726 100%);
  transform: translateY(-5px);
  box-shadow: 0 18px 45px rgba(255, 56, 92, 0.5), 0 10px 25px rgba(255, 56, 92, 0.3);
}

.show-more-btn {
  padding: 12px 18px;
  background: rgba(255, 56, 92, 0.1);
  border: 2px solid rgba(255, 56, 92, 0.3);
  border-radius: 30px;
  font-size: 14px;
  font-weight: 600;
  color: #FF385C;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(15px);
  text-shadow: none;
  box-shadow: 0 4px 12px rgba(255, 56, 92, 0.15);
}

.show-more-btn:hover {
  border-color: rgba(255, 56, 92, 0.5);
  background: rgba(255, 56, 92, 0.15);
  color: #FF2A52;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 56, 92, 0.25);
}

.filter-actions {
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
}

.clear-filters-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
  backdrop-filter: blur(10px);
}

.clear-filters-btn:hover {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
}

.clear-filters-btn:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .filter-section {
    gap: 0.75rem;
  }
  
  .filter-chips {
    gap: 0.6rem;
  }
  
  .filter-chip {
    font-size: 14px;
    padding: 12px 16px;
  }
  
  .filter-select {
    max-width: 100%;
  }
}
</style>