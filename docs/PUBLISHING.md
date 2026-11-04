# Publishing `networkluki-cipher` to PyPI

Publishing requires repository maintainer access and a PyPI account. **Do not store a PyPI API token in the repository.** The release workflow uses GitHub Actions OIDC Trusted Publishing.

## 1. Prepare PyPI and GitHub

1. Confirm that the distribution name `networkluki-cipher` is available. A name not found by a public search may still be reserved or blocked by PyPI.
2. In GitHub, configure the environment named `pypi`. Restrict deployment to release tags and add required reviewers where your plan permits.
3. On <https://pypi.org/manage/account/publishing/>, add a **pending Trusted Publisher** for a new project (or configure the existing project's publisher if already created):
   - PyPI project name: `networkluki-cipher`
   - Owner: `networkluki`
   - Repository: `cryptography`
   - Workflow filename: `release.yml`
   - Environment: `pypi`
4. Review `.github/workflows/release.yml` and the dependency changes before creating a release. A pending publisher does not reserve the project name.

## 2. Verify locally

From the repository root:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m pip install build twine
python -m build
python -m twine check --strict dist/*
```

Check the build artifacts and ensure they include only the intended Python package and license. CI also tests the distribution and checks the metadata.

## 3. Create a release

1. Merge the PR and confirm CI passes on `main`.
2. Update the `version` in `pyproject.toml` for every new release (versions cannot be overwritten on PyPI).
3. Create and publish a GitHub release tagged **`v<version>`**, e.g. `v0.1.0`, pointing to the reviewed commit.
4. `.github/workflows/release.yml` builds and tests the distributions, verifies that the tag matches `pyproject.toml`, then publishes from the protected `pypi` environment via OIDC.
5. Confirm the release at <https://pypi.org/project/networkluki-cipher/> and test installation in a clean virtual environment.

The action does **not** publish on pushes or pull requests. No API token is necessary, and PyPA's publishing action generates provenance attestations automatically by default.

## Reference

- <https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/>
- <https://docs.pypi.org/trusted-publishers/using-a-publisher/>
- <https://packaging.python.org/en/latest/guides/packaging-projects/>
