# LeetCode Search UI

A Vue 3 frontend web application for browsing and searching LeetCode problems with advanced filtering capabilities.

## 🚀 Features

- **Smart Search**: Search problems by title, description, tags, patterns, or companies
- **Advanced Filtering**: Filter by difficulty, problem types, patterns, and companies
- **Multiple Sort Options**: Sort by recency, difficulty, title, or problem ID
- **Database Management**: Upload and update problem database via JSON/CSV files
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Data Persistence**: Uploaded data persists using localStorage

## 🛠 Tech Stack

- **Vue 3** with Composition API
- **JavaScript ES6+**
- **CSS3** with responsive design
- **JSON/CSV** data storage
- **localStorage** for data persistence

## 📁 Project Structure

```
lc_search_ui/
├── public/
│   └── data/
│       ├── problems.json    # Sample LeetCode problems data
│       └── schema.json      # Data structure schema
├── src/
│   ├── components/
│   │   ├── SearchBar.vue    # Search input and sort controls
│   │   ├── FilterPanel.vue  # Advanced filtering options
│   │   ├── ProblemList.vue  # Results display container
│   │   ├── ProblemCard.vue  # Individual problem display
│   │   └── DataManager.vue  # File upload and data management
│   ├── App.vue              # Main application component
│   └── main.js              # Application entry point
├── netlify.toml             # Netlify deployment configuration
└── package.json
```

## 🚀 Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd lc_search_ui
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run serve
   ```

4. **Open your browser**
   Navigate to `http://localhost:8080`

### Building for Production

```bash
npm run build
```

This creates a `dist` folder with production-ready files.

### Preview Production Build

```bash
npm run preview
```

## 🌐 Deployment

### Netlify (Recommended)

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**
   - Connect your GitHub repository to Netlify
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Deploy automatically on push

   Or use Netlify CLI:
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=dist
   ```

### Other Platforms

The built `dist` folder can be deployed to any static hosting service:
- Vercel
- GitHub Pages
- Firebase Hosting
- AWS S3 + CloudFront

## 📊 Data Format

### JSON Format
```json
[
  {
    "id": 1,
    "title": "Two Sum",
    "difficulty": "Easy",
    "url": "https://leetcode.com/problems/two-sum/",
    "tags": ["Array", "Hash Table"],
    "patterns": ["Two Pointers", "Hash Map"],
    "companies": ["Google", "Amazon", "Microsoft"],
    "dateAdded": "2023-01-01",
    "description": "Problem description..."
  }
]
```

### CSV Format
```csv
id,title,difficulty,url,tags,patterns,companies,dateAdded,description
1,Two Sum,Easy,https://leetcode.com/problems/two-sum/,Array;Hash Table,Two Pointers;Hash Map,Google;Amazon,2023-01-01,Problem description
```

**Note**: Use semicolons (`;`) to separate multiple values in tags, patterns, and companies fields.

## 🎯 Usage

### Basic Search
- Type keywords in the search bar to find problems by title or description
- Search also matches tags, patterns, and company names

### Filtering
- **Difficulty**: Filter by Easy, Medium, or Hard
- **Tags**: Select problem types (Array, DP, Graph, etc.)
- **Patterns**: Filter by algorithmic patterns (Two Pointers, Sliding Window, etc.)
- **Companies**: Filter by companies that frequently ask these problems

### Sorting
- **Latest First**: Sort by date added (newest first)
- **Difficulty**: Easy → Medium → Hard
- **Title**: Alphabetical order (A → Z)
- **Problem ID**: Numerical order

### Database Management
1. Click "Show Database Manager"
2. Upload a JSON or CSV file with your problems
3. Download sample files for reference
4. Data persists between browser sessions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Feedback

Found a bug or have a suggestion? Please [create an issue](https://github.com/your-username/lc_search_ui/issues) on GitHub.

---

Built with ❤️ using Vue 3
