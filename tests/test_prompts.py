"""Kubernetes Operator Agent unit tests module."""
import pytest
from k8s_agent.prompts import SYSTEM_PROMPT

def test_prompt_exists():
    """Test that `SYSTEM_PROMPT` is defined and contains non-empty content.

    Ensures that the `SYSTEM_PROMPT` constant exists, is a string, and
    is not empty after stripping any surrounding whitespace.

    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert SYSTEM_PROMPT is not None
    assert isinstance(SYSTEM_PROMPT, str)
    assert len(SYSTEM_PROMPT.strip()) > 0

def test_prompt_contains_helm():
    """
    Test that SYSTEM_PROMPT contains helm-related instructions.

    Verifies the presence of key helm-related operations such as 'helm list',
    the use of helm for installations, updates, and deletions of applications.

    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert "helm list --all-namespaces" in SYSTEM_PROMPT
    assert "helm && kubectl" in SYSTEM_PROMPT
    assert "Applications can be installed, updated and deleted with helm" in SYSTEM_PROMPT

def test_prompt_contains_kubectl():
    """
    Test that SYSTEM_PROMPT contains kubectl-related instructions.

    Ensures that the SYSTEM_PROMPT includes kubectl commands for querying and
    managing Kubernetes resources, including CRDs and other resource types.

    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert "kubectl get CustomResourceDefinitions" in SYSTEM_PROMPT
    assert "kubectl explain (with --recursive=true)" in SYSTEM_PROMPT
    assert "kubectl get deployments,statefulset,daemonsets,services" in SYSTEM_PROMPT

def test_prompt_instructions():
    """
    Test that SYSTEM_PROMPT contains key instruction sections.

    Verifies the presence of specific instructional guidance, including usage
    of the terminal function, explanations of commands, and decision-making
    based on the current cluster state.

    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert "always explain which commands you are about to run" in SYSTEM_PROMPT
    assert "Specify namespaces explicitly during helm or kubectl" in SYSTEM_PROMPT

def test_prompt_avoidance_section():
    """
    Test that SYSTEM_PROMPT contains avoidance instructions.

    Ensures that SYSTEM_PROMPT includes instructions to avoid prompting users
    for input, explaining how to do things, or asking users to take actions.

    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert "Avoid the following:" in SYSTEM_PROMPT
    assert "- prompting the user for input" in SYSTEM_PROMPT
    assert "- explain to the user how to do things" in SYSTEM_PROMPT
    assert "- asking the user to do things" in SYSTEM_PROMPT

@pytest.mark.parametrize("keyword", [
    "CurrentClusterState", "terminal function", "bash pipes",
    "stable release", "search the internet", "CustomResourceDefinitions"
])
def test_prompt_keywords(keyword):
    """
    Parameterized test for ensuring key terms in SYSTEM_PROMPT.

    This test checks if essential concepts and keywords like 'CurrentClusterState'
    and 'bash pipes' are present in the SYSTEM_PROMPT content.

    :param str keyword:
       The parametrized keyword string.
    :var str SYSTEM_PROMPT:
       The prompt provided to the LLM system.
    """
    assert keyword in SYSTEM_PROMPT
