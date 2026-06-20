import pytest

from skillops.versioning.create_skill_version import create_skill_version, next_version
from skillops.versioning.compare_skill_versions import compare_skill_versions
from skillops.versioning.write_changelog import write_changelog
from skillops.versioning.rollback_skill import rollback_skill, active_version, set_active_version


def _seed(skills_root, skill="incident-triage"):
    vdir = skills_root / skill / "versions"
    vdir.mkdir(parents=True)
    (vdir / "v1.skill.md").write_text("# v1\nurgent := high or impact\n")
    return skill


def test_create_skill_version_increments(tmp_path):
    skill = _seed(tmp_path)
    assert next_version(skill, str(tmp_path)) == "v2"
    log = str(tmp_path / "changelog.md")
    res = create_skill_version(skill, "# v2\nnew\n", reason="corrective", skills_root=str(tmp_path), changelog_path=log)
    assert res["version"] == "v2"
    assert (tmp_path / skill / "versions" / "v2.skill.md").exists()
    assert "v2" in (tmp_path / "changelog.md").read_text()


def test_create_version_refuses_overwrite(tmp_path):
    skill = _seed(tmp_path)
    log = str(tmp_path / "changelog.md")
    with pytest.raises(FileExistsError):
        create_skill_version(skill, "# v1 again\n", version="v1", reason="x", skills_root=str(tmp_path), changelog_path=log)


def test_compare_versions(tmp_path):
    skill = _seed(tmp_path)
    create_skill_version(skill, "# v2\nurgent := high or impact\nextra line\n",
                         reason="r", skills_root=str(tmp_path), changelog_path=str(tmp_path / "c.md"))
    diff = compare_skill_versions(skill, "v1", "v2", skills_root=str(tmp_path))
    assert diff["changed"] is True
    assert diff["lines_added"] >= 1


def test_write_changelog_appends(tmp_path):
    path = str(tmp_path / "log.md")
    write_changelog("incident-triage", from_version="v1", to_version="v2", reason="r", changelog_path=path)
    write_changelog("incident-triage", from_version="v2", to_version="v3", reason="r2", changelog_path=path)
    text = open(path).read()
    assert "v2" in text and "v3" in text


def test_rollback_reversible(tmp_path):
    skill = _seed(tmp_path)
    create_skill_version(skill, "# v2\nx\n", reason="r", skills_root=str(tmp_path), changelog_path=str(tmp_path / "c.md"))
    set_active_version(skill, "v2", str(tmp_path))
    assert active_version(skill, str(tmp_path)) == "v2"
    res = rollback_skill(skill, "v1", skills_root=str(tmp_path), changelog_path=str(tmp_path / "c.md"))
    assert res["active_version"] == "v1"
    assert active_version(skill, str(tmp_path)) == "v1"


def test_rollback_missing_version_raises(tmp_path):
    skill = _seed(tmp_path)
    with pytest.raises(FileNotFoundError):
        rollback_skill(skill, "v9", skills_root=str(tmp_path), changelog_path=str(tmp_path / "c.md"))
