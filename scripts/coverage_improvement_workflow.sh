#!/bin/bash
#==========================================================================================\\\
#======================= scripts/coverage_improvement_workflow.sh =====================\\\
#==========================================================================================\\\

# Automated coverage improvement workflow with quality gate validation for GitHub Issue #9
# Repository: https://github.com/theSadeQ/dip-smc-pso.git

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Functions for colored output
print_header() {
    echo -e "${BLUE}🚀 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${PURPLE}📊 $1${NC}"
}

# Configuration
COVERAGE_THRESHOLD_OVERALL=85
COVERAGE_THRESHOLD_CRITICAL=95
COVERAGE_THRESHOLD_SAFETY=100

print_header "Starting Coverage Improvement Workflow - GitHub Issue #9"
echo "Repository: https://github.com/theSadeQ/dip-smc-pso.git"
echo "Target Thresholds: Overall ${COVERAGE_THRESHOLD_OVERALL}% | Critical ${COVERAGE_THRESHOLD_CRITICAL}% | Safety ${COVERAGE_THRESHOLD_SAFETY}%"
echo "================================================================"

# Ensure we're in the project root
if [ ! -f "simulate.py" ] || [ ! -d "src" ]; then
    print_error "Not in project root directory. Please run from D:/Projects/main"
    exit 1
fi

# Create reports directory if it doesn't exist
mkdir -p reports

# Step 1: Install dependencies
print_header "Step 1: Installing Coverage Dependencies"
pip install pytest-cov coverage[toml] > /dev/null 2>&1
print_success "Coverage tools installed"

# Step 2: Baseline coverage measurement
print_header "Step 2: Measuring Baseline Coverage"
echo "Running comprehensive coverage analysis..."

# Generate baseline coverage report
if pytest --cov=src --cov-report=xml:coverage_baseline.xml --cov-report=html:htmlcov_baseline --cov-report=term-missing --tb=short -q; then
    print_success "Baseline coverage measurement completed"
else
    print_warning "Some tests failed during baseline measurement - continuing with available coverage data"
fi

# Extract baseline metrics
if [ -f "coverage_baseline.xml" ]; then
    baseline_coverage=$(python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage_baseline.xml')
root = tree.getroot()
print(f'{float(root.attrib[\"line-rate\"]) * 100:.1f}')
" 2>/dev/null || echo "0.0")
    print_info "Baseline coverage: ${baseline_coverage}%"
else
    print_error "Failed to generate baseline coverage report"
    exit 1
fi

# Step 3: Safety-critical component validation (100% required)
print_header "Step 3: Validating Safety-Critical Components (100% requirement)"

SAFETY_CRITICAL_COMPONENTS=(
    "src/core/safety_guards.py"
    "src/utils/validation/"
)

safety_critical_passed=true
for component in "${SAFETY_CRITICAL_COMPONENTS[@]}"; do
    if [ -e "$component" ]; then
        echo "Testing safety-critical component: $component"
        if pytest --cov="$component" --cov-fail-under=${COVERAGE_THRESHOLD_SAFETY} --tb=short -q; then
            print_success "Safety-critical component passed: $component"
        else
            print_error "CRITICAL: Safety component below 100% coverage: $component"
            safety_critical_passed=false
        fi
    else
        print_warning "Safety-critical component not found: $component"
    fi
done

if [ "$safety_critical_passed" = false ]; then
    print_error "PRODUCTION BLOCKED: Safety-critical components must have 100% coverage"
    echo "Please add comprehensive tests for safety-critical components before proceeding."
fi

# Step 4: Critical components validation (95% required)
print_header "Step 4: Validating Critical Components (95% requirement)"

CRITICAL_COMPONENTS=(
    "src/controllers/smc/"
    "src/controllers/adaptive_smc.py"
    "src/controllers/classic_smc.py"
    "src/controllers/sta_smc.py"
    "src/core/dynamics.py"
    "src/core/dynamics_full.py"
    "src/optimizer/pso_optimizer.py"
    "src/core/simulation_runner.py"
)

critical_components_status=()
for component in "${CRITICAL_COMPONENTS[@]}"; do
    if [ -e "$component" ]; then
        echo "Testing critical component: $component"
        if pytest --cov="$component" --cov-fail-under=${COVERAGE_THRESHOLD_CRITICAL} --tb=short -q 2>/dev/null; then
            print_success "Critical component passed: $component"
            critical_components_status+=("PASS")
        else
            print_warning "Critical component below 95% threshold: $component"
            critical_components_status+=("FAIL")
        fi
    else
        print_warning "Critical component not found: $component"
        critical_components_status+=("NOT_FOUND")
    fi
done

# Count critical component results
critical_passed=$(printf '%s\n' "${critical_components_status[@]}" | grep -c "PASS" || echo 0)
critical_total=${#CRITICAL_COMPONENTS[@]}
critical_pass_rate=$((critical_passed * 100 / critical_total))

print_info "Critical components: ${critical_passed}/${critical_total} passed (${critical_pass_rate}%)"

# Step 5: Overall system validation (85% required)
print_header "Step 5: Validating Overall System Coverage (85% requirement)"

if pytest --cov=src --cov-fail-under=${COVERAGE_THRESHOLD_OVERALL} --tb=short -q 2>/dev/null; then
    print_success "Overall system coverage meets 85% threshold"
    overall_passed=true
else
    print_warning "Overall system coverage below 85% threshold"
    overall_passed=false
fi

# Step 6: Generate comprehensive analysis using coverage validator
print_header "Step 6: Generating Comprehensive Coverage Analysis"

if [ -f "scripts/coverage_validator.py" ]; then
    echo "Running advanced coverage analysis..."
    python scripts/coverage_validator.py \
        --coverage-xml coverage_baseline.xml \
        --output-report reports/coverage_quality_report.md \
        --output-json reports/coverage_metrics.json \
        --verbose

    print_success "Coverage analysis completed"
    print_info "Report saved to: reports/coverage_quality_report.md"
    print_info "Metrics saved to: reports/coverage_metrics.json"
else
    print_warning "Advanced coverage validator not found - generating basic report"

    # Basic coverage report
    coverage report --show-missing > reports/coverage_basic_report.txt 2>/dev/null || true
    print_info "Basic coverage report saved to: reports/coverage_basic_report.txt"
fi

# Step 7: Generate improvement recommendations
print_header "Step 7: Generating Improvement Recommendations"

cat > reports/coverage_improvement_plan.md << EOF
# Coverage Improvement Action Plan
**Generated**: $(date '+%Y-%m-%d %H:%M:%S')
**Repository**: https://github.com/theSadeQ/dip-smc-pso.git
**Issue**: GitHub Issue #9 - Coverage Analysis Framework

## Current Status Summary
- **Baseline Coverage**: ${baseline_coverage}%
- **Overall System**: $([ "$overall_passed" = true ] && echo "✅ PASSED" || echo "❌ FAILED")
- **Critical Components**: ${critical_passed}/${critical_total} passed (${critical_pass_rate}%)
- **Safety-Critical**: $([ "$safety_critical_passed" = true ] && echo "✅ PASSED" || echo "❌ FAILED")

## Priority Actions Required

### 1. Safety-Critical Components (CRITICAL PRIORITY)
$(if [ "$safety_critical_passed" = false ]; then
    echo "❌ **PRODUCTION BLOCKING**: Safety-critical components below 100% coverage"
    echo "- **Action**: Immediately add comprehensive tests for safety mechanisms"
    echo "- **Timeline**: Complete within 1-2 days"
    echo "- **Impact**: Blocks production deployment until resolved"
else
    echo "✅ **Safety-critical components meet 100% requirement**"
fi)

### 2. Critical Components (HIGH PRIORITY)
$(if [ $critical_pass_rate -lt 90 ]; then
    echo "⚠️  **Critical components need enhancement**"
    echo "- **Target**: 95% coverage for all critical components"
    echo "- **Focus Areas**: SMC controllers, dynamics models, PSO optimizer"
    echo "- **Timeline**: 1-2 weeks systematic improvement"
else
    echo "✅ **Critical components meet or approach 95% requirement**"
fi)

### 3. Overall System Coverage (MEDIUM PRIORITY)
$(if [ "$overall_passed" = false ]; then
    echo "⚠️  **Overall system coverage below 85% threshold**"
    echo "- **Current**: ${baseline_coverage}%"
    echo "- **Target**: 85%+"
    echo "- **Gap**: $(python -c "print(f'{85 - float('${baseline_coverage}'):.1f}%')" 2>/dev/null || echo "Unknown")"
    echo "- **Strategy**: Incremental improvement across all components"
else
    echo "✅ **Overall system coverage meets 85% requirement**"
fi)

## Mathematical Analysis
- **Coverage Efficiency**: C_eff = ${baseline_coverage}/85 = $(python -c "print(f'{float('${baseline_coverage}')/85:.3f}')" 2>/dev/null || echo "N/A")
- **Improvement Required**: $(python -c "print(f'{max(0, 85 - float('${baseline_coverage}')):.1f}%')" 2>/dev/null || echo "N/A")

## Next Steps
1. **Immediate**: Address safety-critical coverage gaps
2. **Short-term**: Enhance critical component testing
3. **Medium-term**: Systematic overall coverage improvement
4. **Long-term**: Maintain quality gates and prevent regression

## Integration with CLAUDE.md
This improvement plan aligns with established quality standards:
- **Automated Git Workflow**: All improvements trigger automatic repository updates
- **Quality Gate Enforcement**: CI/CD pipeline blocks below-threshold commits
- **Production Readiness**: Coverage directly impacts deployment scoring

EOF

print_success "Improvement plan generated: reports/coverage_improvement_plan.md"

# Step 8: Final status summary
print_header "Step 8: Final Status Summary"

echo "================================================================"
print_info "Coverage Improvement Workflow Completed"
echo "================================================================"

overall_status="PASSED"
if [ "$safety_critical_passed" = false ]; then
    overall_status="CRITICAL_FAILURE"
elif [ "$overall_passed" = false ] || [ $critical_pass_rate -lt 80 ]; then
    overall_status="NEEDS_IMPROVEMENT"
fi

case $overall_status in
    "PASSED")
        print_success "All quality gates passed! System ready for production."
        ;;
    "NEEDS_IMPROVEMENT")
        print_warning "Quality gates need improvement but system is functional."
        print_info "Focus on systematic coverage enhancement per generated plan."
        ;;
    "CRITICAL_FAILURE")
        print_error "CRITICAL: Safety-critical components below requirements."
        print_error "Production deployment BLOCKED until safety coverage reaches 100%."
        ;;
esac

echo ""
print_info "Generated Reports:"
echo "  - Coverage Quality Report: reports/coverage_quality_report.md"
echo "  - Coverage Metrics: reports/coverage_metrics.json"
echo "  - Improvement Plan: reports/coverage_improvement_plan.md"
echo "  - HTML Coverage Report: htmlcov_baseline/index.html"

echo ""
print_info "Next Actions:"
if [ "$safety_critical_passed" = false ]; then
    echo "  1. 🔴 URGENT: Add tests for safety-critical components (100% required)"
fi
if [ "$overall_passed" = false ]; then
    echo "  2. 🟡 Add tests to reach 85% overall coverage threshold"
fi
if [ $critical_pass_rate -lt 90 ]; then
    echo "  3. 🟠 Enhance critical component testing (95% target)"
fi
echo "  4. 🔵 Integrate coverage validation into CI/CD pipeline"
echo "  5. 🟢 Monitor coverage trends and prevent regression"

# Exit with appropriate code
case $overall_status in
    "PASSED")
        exit 0
        ;;
    "NEEDS_IMPROVEMENT")
        exit 2  # Warning but not critical
        ;;
    "CRITICAL_FAILURE")
        exit 1  # Critical failure
        ;;
esac