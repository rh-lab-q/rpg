This document is purely for testig purposes, please do not take it seriously
============================================================================

Variables for tests:

VAR_TEST6 = [test6 > test5]

VAR_TEST7 = [
			test7.1
			[test7.2]
]

VAR_TEST8.1 = "test8.1 = doNotKnowIfViableButItWorks [$VAR_TEST8.2]"

VAR_TEST8.2 = "test8.2"


Something to be skipped:

AC_MSG_CHECKING([For something 0.5.3 ABI break])
AC_TRY_COMPILE([#include <stdlib.h>
#include <something/sack.h>],
               [hy_sack_create(NULL, NULL, NULL, 0); return 0;],
               [AC_MSG_RESULT([no]); BUILDOPT_SOMETHING_SACK_CREATE2=0],
               [AC_MSG_RESULT([yes]); BUILDOPT_SOMETHING_SACK_CREATE2=1])
AC_DEFINE_UNQUOTED(BUILDOPT_SOMETHING_SACK_CREATE2, $BUILDOPT_SOMETHING_SACK_CREATE2, [something ABI change])
AC_PATH_PROG([XSLTPROC], [xsltproc])
AC_ARG_ENABLE(dnf-yumdb, AS_HELP_STRING([--enable-dnf-yumdb],[use dnf/yumdb instead of yum/yumdb @<:@default=yes@:>@]),
              enable_dnf_yumdb=$enableval,enable_dnf_yumdb=yes)
if test x$enable_dnf_yumdb = xyes; then
  AC_DEFINE_UNQUOTED(BUILDOPT_USE_DNF_YUMDB,1,[Use dnf/yumdb instead of yum/yumdb])
fi

Tests:

PKG_CHECK_MODULES(TEST1, test1 >= 2.36.0)

PKG_CHECK_MODULES(TEST2,
				  test2.1 >= test1.0
				  test2.2)

PKG_CHECK_MODULES(TEST3, test3.1 >= 0.4.6 [test3.2 >= 1.7.11]
						 test3.3 >= 4.11.0, useless text)


PKG_CHECK_MODULES(EMPTYTEST, )

PKG_CHECK_MODULES(TEST4, test4 <= test5, another useless text, and another)

PKG_CHECK_MODULES(TEST5, test5.1
						 [ test5.2 ]
					   , pure uselessness)

PKG_CHECK_MODULES(TEST6, [$VAR_TEST6])

PKG_CHECK_MODULES(TEST7, [$VAR_TEST7] test7.3)

PKG_CHECK_MODULES(TEST8, [$VAR_TEST8.1])

PKG_CHECK_MODULES(TEST9, ,PKG_CHECK_MODULES(TEST9, test9.1), PKG_CHECK_MODULES(TEST9, test9.2))
