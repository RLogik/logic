#!/usr/bin/env bash

##############################################################################
#
#    DESCRIPTION: Library of methods specifically for the project.
#    Include using source .whales/.lib.sh
#
##############################################################################

source .whales/.lib.sh;

##############################################################################
# GLOBAL VARIABLES
##############################################################################

export PATH_SOURCE="src";
export PATH_TEST="test";
env_from ".env" import REQUIREMENTS_PY AS PATH_REQ_PY;
env_from ".env" import CONFIG as PATH_CONFIG;
env_from ".env" import TESTCONFIG as PATH_TESTCONFIG;
env_from ".env" import UNITTEST_SCHEMA as UNITTEST_SCHEMA;


##############################################################################
# AUXILIAR METHODS: Python
##############################################################################

function call_python() {
    ( is_linux ) && python3 $@ || py -3 $@;
}

function call_pipinstall() {
    call_python -m pip install $@;
}

function call_utest() {
    call_python -m unittest discover $@;
}

##############################################################################
# AUXILIARY METHODS: CLEANING
##############################################################################

function clean_by_pattern() {
    path="$1";
    pattern="$2"
    force="$3";
    if ( ls $path | grep -q -E "$pattern" ); then
        if [[ "$force" == "true" ]]; then
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print "    \033[94m" PATH "/" $1 "\033[0m"}' >> $OUT;
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print PATH "/" $1}' | xargs rm -r;
        else
            _log_info "Files to be removed:";
            ls $path | grep -E "$pattern" | awk -v PATH=$path '{print "    \033[94m" PATH "/" $1 "\033[0m"}' >> $OUT;
            _cli_ask "Do you wish to proceed? (y/n) "
            read answer;
            if ( check_answer "$answer" ); then
                _log_info "Deleting...";
                ls $path | grep -E "$pattern" | awk -v PATH=$path '{print PATH "/" $1}' | xargs rm -r;
            else
                _log_info "Skipping.";
            fi
        fi
    fi
}

function garbage_collection_python() {
    objects=( $(ls {,**/,**/**/}*.pyo 2> $VERBOSE) );
    n=${#objects[@]};
    _cli_message "    (\033[91mforce removed\033[0m) $n x \033[94m.pyo\033[0m files";
    [ "$n" == "0" ] || ls {,**/,**/**/}*.pyo 2> $VERBOSE | awk '{print $1}' | xargs rm;

    objects=( $(find * -type d -name *__pycache__) );
    n=${#objects[@]};
    _cli_message "    (\033[91mforce removed\033[0m) $n x \033[94m__pycache__\033[0m folders";
    [ "$n" == "0" ] || find * -type d -name *__pycache__ | awk '{print $1}' | xargs rm -rf;
}

##############################################################################
# MAIN METHODS: PROCESSES
##############################################################################

function run_setup() {
    _log_info "SETUP"
    _log_info "Check requirements";
    call_pipinstall "$( cat ${PATH_REQ_PY} )";
}

function run_explore_console() {
    _log_info "READY TO EXPLORE.";
    $CMD_EXPLORE;
}

function run_main() {
    cwd="$PWD";
    pushd "$PATH_SOURCE" >> $VERBOSE
        call_python main.py "$cwd/$PATH_CONFIG";
    popd >> $VERBOSE
}

function run_test_unit() {
    asverbose=$1;
    verboseoption="";
    ( $asverbose ) && verboseoption="-v";
    _log_info "UNITTESTS";
    local output="$(call_utest              \
        $verboseoption                      \
        --top-level-directory "."           \
        --start-directory "${PATH_TEST}"   \
        --pattern "${UNITTEST_SCHEMA}" 2>&1 \
    )";
    echo -e "$output";
    ( echo "$output" | grep -E -q "^[[:space:]]*(FAIL:|FAILED)" ) \
        && _log_fail "Unit tests failed!";
    _log_info "Unit tests erfolgreich!";
    return 0;
}

function run_test_e2e() {
    cwd="$PWD";
    _log_info "E2E TESTS";
    pushd "$PATH_TEST" >> $VERBOSE
        call_python e2e.py "$cwd/$PATH_TESTCONFIG";
    popd >> $VERBOSE
}

function run_clean_artefacts() {
    _log_warn "Clean process not yet implemented!";
    _log_info "CLEAN ARTEFACTS";
    garbage_collection_python
}
