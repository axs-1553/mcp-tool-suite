# Swiss Army Knife

A versatile collection of Python scripts for various tasks. Each script is self-contained and follows a consistent interface pattern.

## Available Scripts

### AI and Swarm Tools
- **ai-swarm.sak.py**: Basic AI swarm management with agent creation, task distribution, and output collection
- **enhanced-swarm.sak.py**: Advanced swarm management with persistent daemon process and priority-based scheduling
- **swarm.sak.py**: AI swarm framework for parallel task processing
- **swarm-manager.sak.py**: Asynchronous AI swarm agent management with state tracking

### GitHub Tools
- **github.sak.py**: Comprehensive GitHub operations (create repos, files, issues, PRs)
- **github-list-repos.sak.py**: List public repositories for GitHub users

### Data Tools
- **transform.sak.py**: Advanced data transformation between formats (JSON, CSV, YAML, XML, etc.)
- **visualize.sak.py**: Enhanced data visualization with multiple plot types
- **kvstore.sak.py**: Simple persistent key-value store

## Features By Tool

### AI Swarm Tools
- Create and manage AI agent swarms
- Task distribution and collection
- Status monitoring
- Role-based organization
- Performance metrics
- Error logging
- Priority-based scheduling
- Dependency management
- Parallel task processing

### GitHub Tools
- Repository creation and management
- File creation and updates
- Issue and PR management
- Repository forking
- Public repository listing

### Data Tools
#### Transform
- Multiple format support: JSON, CSV, YAML, XML, TXT, EXCEL, SQL
- Schema validation
- Data filtering and aggregation
- Column/field selection
- Smart type inference
- Batch processing
- Delta detection

#### Visualize
- Multiple plot types: line, bar, scatter, box, violin, heatmap, pie, area, radar, donut
- Multiple subplots and layouts
- Custom color palettes
- Stacked charts
- Data insights
- Interactive plotting

#### Key-Value Store
- Persistent storage
- Basic CRUD operations
- Simple interface
- JSON-based storage

## Usage

1. View available scripts:
   ```bash
   swiss-army-knife --list
   ```

2. Get help for a specific script:
   ```bash
   swiss-army-knife --info <script_name>
   ```

3. Run a script:
   ```bash
   swiss-army-knife <script_name> [arguments]
   ```

## Script Creation Guide

1. Name your script with `.sak.py` extension
2. Include `--info` argument support
3. Provide clear documentation
4. Follow consistent interface pattern
5. Place in the swiss-army-files directory

## Core Features

- Modular design
- Consistent interface
- Self-documenting scripts
- Easy extensibility
- Cross-platform compatibility
- Daemon support for long-running tasks
- Performance monitoring
- Error handling and logging