# 🤝 Contributing to Travix-AI

First off, thank you for considering contributing to Travix-AI! It's people like you that make Travix-AI such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the community

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- A Groq API key

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the 'Fork' button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/travix-ai.git
   cd travix-ai
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/original/travix-ai.git
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Set up backend**
   ```bash
   cd apps/backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add your GROQ_API_KEY to .env
   ```

6. **Set up frontend**
   ```bash
   cd apps/frontend
   npm install
   ```

7. **Run the application**
   ```bash
   # Terminal 1 - Backend
   cd apps/backend
   python -m uvicorn app.main:app --reload --port 8000

   # Terminal 2 - Frontend
   cd apps/frontend
   npm run dev
   ```

---

## 💡 How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check the documentation
- Search existing issues
- Try to reproduce the bug

**When submitting a bug report, include:**
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, Node version)

### Suggesting Features

**Feature suggestions should include:**
- Clear description of the feature
- Use case and motivation
- Possible implementation approach
- Any alternatives considered

### Adding New Features

#### Adding a New Agent

1. **Create agent file**
   ```python
   # apps/backend/app/services/your_agent.py
   
   from typing import List, Dict, Any
   from pydantic import BaseModel
   
   class ToolResult(BaseModel):
       action: str
       message: str
       data: Any
       trace: List[Dict]
   
   class YourAgent:
       def __init__(self):
           pass
       
       def execute(self, user_message: str) -> ToolResult:
           # Your agent logic here
           pass
   ```

2. **Register in orchestrator**
   ```python
   # apps/backend/app/services/groq_orchestrator.py
   
   AGENTS = {
       "your_agent": AgentDefinition(
           name="Your Agent",
           description="What your agent does",
           capabilities=["capability1", "capability2"],
           icon="Y"
       )
   }
   ```

3. **Add API endpoints**
   ```python
   # apps/backend/app/api/orchestrator.py
   
   @router.post("/execute/your_tool")
   async def execute_your_tool(request: YourRequest):
       agent = YourAgent()
       result = agent.execute_tool(request)
       return result.model_dump()
   ```

4. **Add frontend components**
   ```typescript
   // apps/frontend/src/components/dashboard/YourResultView.tsx
   
   export function YourResultView({ data }: Props) {
       // Your UI component
   }
   ```

#### Adding New Flight Routes

1. Edit `apps/backend/app/services/sbt_agent.py`
2. Add to `MOCK_FLIGHTS` dictionary:
   ```python
   ("city1", "city2"): [
       Flight(
           id="UNIQUE-ID",
           airline="Airline Name",
           # ... other fields
       ),
   ]
   ```
3. Run tests: `python test_flight_routes.py`

#### Adding New Hotels

1. Edit `apps/backend/app/services/backoffice_agent.py`
2. Add to `MOCK_HOTELS` dictionary
3. Test with API call

---

## 🎨 Code Style Guidelines

### Python (Backend)

**Follow PEP 8:**
```python
# Good
def search_flights(from_city: str, to_city: str) -> List[Flight]:
    """Search flights between two cities.
    
    Args:
        from_city: Origin city name
        to_city: Destination city name
        
    Returns:
        List of available flights
    """
    # Implementation
    pass

# Bad
def searchFlights(fromCity,toCity):
    # Implementation
    pass
```

**Key points:**
- Use type hints
- Write docstrings for functions and classes
- Use meaningful variable names
- Keep functions focused and small
- Maximum line length: 100 characters

### TypeScript/React (Frontend)

**Follow Airbnb style guide:**
```typescript
// Good
interface FlightProps {
  flight: Flight;
  onSelect: (flight: Flight) => void;
}

export function FlightCard({ flight, onSelect }: FlightProps) {
  const handleClick = () => {
    onSelect(flight);
  };

  return (
    <div className="flight-card">
      {/* Component content */}
    </div>
  );
}

// Bad
export function FlightCard(props) {
  return <div>{props.flight.name}</div>
}
```

**Key points:**
- Use functional components with hooks
- Define proper TypeScript interfaces
- Use meaningful component and variable names
- Keep components focused
- Use TailwindCSS for styling

### File Naming

- Python: `snake_case.py`
- TypeScript/React: `PascalCase.tsx` for components, `camelCase.ts` for utilities
- CSS: `kebab-case.css`

---

## 📝 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(flight): add support for multi-city flights

- Added multi-city route support
- Updated UI to handle multiple destinations
- Added tests for multi-city booking

Closes #123
```

```bash
fix(hotel): correct price calculation for weekend bookings

Weekend prices were not being applied correctly due to
timezone conversion issue.

Fixes #456
```

```bash
docs(readme): update installation instructions

Added Docker setup instructions and troubleshooting section.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   # Backend tests
   python test_flight_routes.py
   
   # Frontend tests (if applicable)
   npm test
   ```

3. **Check code style**
   ```bash
   # Python
   flake8 apps/backend
   black apps/backend
   
   # TypeScript
   npm run lint
   ```

4. **Update documentation**
   - Update README if adding features
   - Add comments to complex code
   - Update API documentation if needed

### Submitting a Pull Request

1. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request on GitHub**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR checklist:**
   - [ ] Code follows style guidelines
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Commit messages follow convention
   - [ ] PR title is clear and descriptive
   - [ ] Linked to relevant issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe testing done

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] My code follows style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests
- [ ] New and existing tests pass
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR

---

## 🧪 Testing Guidelines

### Writing Tests

**Backend tests:**
```python
def test_search_flights():
    """Test flight search functionality"""
    agent = SBTAgent()
    result = agent.search_flights("Delhi", "Mumbai")
    
    assert result.action == "search_flights"
    assert len(result.data['flights']) > 0
    assert result.data['flights'][0]['from_city'] == "Delhi"
```

**Frontend tests:**
```typescript
describe('FlightCard', () => {
  it('should display flight details', () => {
    const flight = mockFlight();
    render(<FlightCard flight={flight} />);
    
    expect(screen.getByText(flight.airline)).toBeInTheDocument();
    expect(screen.getByText(flight.price)).toBeInTheDocument();
  });
});
```

### Running Tests

```bash
# Backend
python test_flight_routes.py

# Frontend
npm test

# Coverage
npm run test:coverage
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TailwindCSS Docs](https://tailwindcss.com/docs)

---

## 💬 Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/travix-ai/discussions)
- Join our [Discord Server](https://discord.gg/travix-ai)
- Email: dev@travix-ai.com

---

## 🎉 Thank You!

Your contributions make Travix-AI better for everyone. We appreciate your time and effort!

---

<div align="center">

**Happy Contributing! 🚀**

</div>
