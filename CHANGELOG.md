# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2024-03-XX

### Changed
- Enhanced table UI with improved hover states and text visibility
- Improved color contrast for better accessibility
- Added smooth transitions for interactive elements
- Refined dark mode colors for better readability
- Updated table cell text colors to ensure visibility in all states

### Fixed
- Text visibility issues on row hover states
- Dark mode contrast issues in table cells
- Inconsistent text colors in table rows

## [1.1.0] - 2024-03-XX

### Added
- DFS (Daily Fantasy Sports) integration
  - New `/api/dfs` endpoints for contests and lineup optimization
  - Player pool management and real-time updates
  - Advanced lineup optimization with customizable constraints
- Modern UI improvements
  - Dark mode support with theme toggle
  - Integration of shadcn/ui components
  - Improved responsive design
- Auto-refresh functionality for live odds updates
- Consistent API routing with `/api` prefix for all endpoints

### Changed
- Updated API routes to use `/api` prefix for better organization
- Enhanced frontend directory structure
- Improved documentation with detailed API endpoints
- Updated installation instructions for clarity

### Fixed
- API routing consistency issues
- Frontend-backend communication paths
- Documentation accuracy for installation steps

## [1.0.0] - 2024-XX-XX

### Added
- Initial release of EV-Arb-Tool
- Core EV calculation pipeline
- Basic web dashboard
- Support for props and MLB betting
- Basic logging functionality 