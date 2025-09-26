# 🔌 MCP Integration Demo

A comprehensive demonstration tool showcasing Model Context Protocol (MCP) integrations with various services. This application demonstrates how MCP servers can be used to connect AI coding agents like Cursor with external services.

## ✨ Features

### 🐙 GitHub Integration
- **Repository Search** - Search for repositories using GitHub's API
- **Repository Details** - Get detailed information about specific repositories
- **Real-time Results** - Live API responses with loading states
- **Interactive UI** - Click to explore repositories directly

### ☁️ Salesforce Integration
- **Organization Information** - Get Salesforce org details and configuration
- **User Information** - Retrieve current user profile and role information
- **Live Data** - Real-time API responses from Salesforce
- **Professional Display** - Clean, organized data presentation

### ⚙️ MCP Configuration Display
- **Server Status** - Visual indicators for all configured MCP servers
- **Connection Status** - Real-time status of each MCP service
- **Configuration Overview** - Complete MCP setup visualization

### 📡 Live API Response Viewer
- **JSON Display** - Formatted API responses for debugging
- **Timestamp Tracking** - When each API call was made
- **Endpoint Information** - Which service was called
- **Real-time Updates** - Live response data

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No additional software required!

### Installation & Running

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd Santhosh-test
   ```

2. **Open the application**
   - Simply open `index.html` in your web browser
   - Or use a local server: `python -m http.server 8000`

3. **Start exploring MCP integrations**
   - Try the GitHub search functionality
   - Test the Salesforce integration buttons
   - View live API responses

## 🔧 MCP Servers Demonstrated

### Working Integrations
- **GitHub** - Repository search and details
- **Salesforce** - Organization and user information

### Configured but Demo-Only
- **AWS Logs** - CloudWatch log analysis
- **Multi-DB** - Database connectivity
- **Kayako Tools** - Support ticket management
- **STAR** - Support ticket assignment and routing
- **Who Is On** - Agent presence tracking

## 🏗️ Technical Architecture

### File Structure
```
Santhosh-test/
├── index.html          # Main application structure
├── style.css           # Modern styling and animations
├── script.js           # MCP integration logic
├── README.md           # This documentation
└── backup/             # Previous project files
```

### Technology Stack
- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with flexbox, grid, and animations
- **Vanilla JavaScript** - No framework dependencies
- **MCP Protocol** - Model Context Protocol integration

### Key Features
- **Responsive Design** - Works on desktop and mobile
- **Loading States** - Visual feedback during API calls
- **Error Handling** - User-friendly error messages
- **Mock Data** - Simulated API responses for demonstration
- **Real-time Updates** - Live data display

## 🎯 How It Works

### MCP Integration Flow
1. **User Interaction** - Click buttons to trigger MCP calls
2. **Loading State** - Visual feedback during API processing
3. **MCP Server Call** - Simulated calls to external services
4. **Data Processing** - Format and structure the response
5. **UI Update** - Display results in user-friendly format
6. **API Response** - Show raw JSON for debugging

### Mock Data System
- **Realistic Responses** - Based on actual API structures
- **Simulated Delays** - Realistic loading times
- **Error Scenarios** - Demonstrates error handling
- **Live Updates** - Dynamic content generation

## 🔍 Usage Examples

### GitHub Integration
```javascript
// Search for repositories
searchGitHubRepos() // Searches for "cursor mcp" by default

// Get repository details
getRepositoryDetails() // Gets details for GLips/Figma-Context-MCP
```

### Salesforce Integration
```javascript
// Get organization information
getSalesforceOrgInfo() // Returns org details and configuration

// Get user information
getSalesforceUserInfo() // Returns current user profile
```

## 🎨 UI Components

### Cards
- **GitHub Card** - Repository search and details
- **Salesforce Card** - Organization and user info
- **MCP Configuration Card** - Server status overview
- **API Response Card** - Live JSON display

### Interactive Elements
- **Search Inputs** - GitHub repository search
- **Action Buttons** - Trigger MCP integrations
- **Status Badges** - Visual connection indicators
- **Loading States** - Animated feedback

## 🔧 Customization

### Adding New MCP Servers
1. Add server configuration to `displayMCPConfiguration()`
2. Create new mock data functions
3. Add display functions for the new service
4. Update the UI with new buttons and containers

### Styling
- Modify `style.css` for visual changes
- Update color scheme in CSS variables
- Add new animations or transitions
- Customize responsive breakpoints

## 📱 Responsive Design

- **Desktop** - Full feature set with side-by-side layout
- **Tablet** - Optimized card layout
- **Mobile** - Stacked layout with touch-friendly buttons

## 🚀 Future Enhancements

- **Real MCP Integration** - Connect to actual MCP servers
- **More Services** - Add AWS, database, and other integrations
- **Authentication** - Add login and token management
- **Data Persistence** - Save and load configurations
- **Advanced Filtering** - Search and filter capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Model Context Protocol** - For the integration framework
- **Cursor** - For the AI coding environment
- **GitHub** - For the repository API
- **Salesforce** - For the CRM integration

---

**Built with ❤️ using MCP (Model Context Protocol)**

*Last updated: September 2024*