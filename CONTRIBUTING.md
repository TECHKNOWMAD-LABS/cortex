# Contributing to Cortex

## Submitting Issues

Report bugs and request features by opening an issue:
- **Bug Reports**: Include steps to reproduce, expected vs actual behavior, and your environment details
- **Feature Requests**: Describe the use case and how the feature should work

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes following the format below
4. Push to your fork and open a pull request against `main`
5. Address review feedback and maintain branch up-to-date with main

## Code Standards

**Python:**
- Use type hints on all function parameters and return values
- Write docstrings for all functions and classes (Google style)
- Avoid bare `except:` clauses; catch specific exceptions
- Use parameterized queries for SQL to prevent injection
- Format code with Black (line length 88)

**General:**
- Keep functions focused and reasonably sized
- Write meaningful variable names
- Add inline comments for non-obvious logic

## Security Requirements

- Never commit secrets (API keys, tokens, credentials)
- Use `defusedxml` for parsing untrusted XML
- Pass `shell=False` to `subprocess` calls
- Validate all user inputs
- Review dependencies before adding

## Testing

- Run `bandit` on all Python code before submitting: `bandit -r .`
- Add tests for new functionality
- Ensure existing tests pass

## Commit Message Format

Use clear, concise messages:
```
Brief summary of changes (50 chars max)

Longer explanation if needed. Explain the why, not just what changed.
```

## License

This project is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same terms.
