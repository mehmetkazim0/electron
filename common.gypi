{
  'includes': [
    'vendor/brightray/brightray.gypi',
  ],
  'variables': {
    # Required by breakpad.
    'os_bsd': 0,
    # Reflects node's config.gypi.
    'component%': 'static_library',
    'python': 'python',
    'openssl_no_asm': 1,
    'node_install_npm': 'false',
    'node_prefix': '',
    'node_shared_cares': 'false',
    'node_shared_http_parser': 'false',
    'node_shared_libuv': 'false',
    'node_shared_openssl': 'false',
    'node_shared_v8': 'true',
    'node_shared_zlib': 'false',
    'node_tag': '',
    'node_use_dtrace': 'false',
    'node_use_etw': 'false',
    'node_use_mdb': 'false',
    'node_use_openssl': 'true',
    'node_use_perfctr': 'false',
    'uv_library': 'static_library',
    'uv_parent_path': 'vendor/node/deps/uv',
    'uv_use_dtrace': 'false',
    'v8_postmortem_support': 'false',
    'v8_enable_i18n_support': 'false',
    # Required by Linux (empty for now, should support it in future).
    'sysroot': '',
  },
  # Settings to compile node under Windows.
  'target_defaults': {
    'target_conditions': [
      ['_target_name in ["libuv", "http_parser", "openssl", "cares", "node", "zlib"]', {
        'msvs_disabled_warnings': [
          4703,  # potentially uninitialized local pointer variable 'req' used
          4013,  # 'free' undefined; assuming extern returning int
          4018,  # signed/unsigned mismatch
          4054,  #
          4057,  # 'function' : 'volatile LONG *' differs in indirection to slightly different base types from 'unsigned long *'
          4189,  #
          4131,  # uses old-style declarator
          4133,  # incompatible types
          4146,  # unary minus operator applied to unsigned type, result still unsigned
          4152,  # function/data pointer conversion in expression
          4206,  # translation unit is empty
          4204,  # non-constant aggregate initializer
          4210,  # nonstandard extension used : function given file scope
          4214,  # bit field types other than int
          4232,  # address of dllimport 'free' is not static, identity not guaranteed
          4291,  # no matching operator delete found
          4295,  # array is too small to include a terminating null character
          4389,  # '==' : signed/unsigned mismatch
          4505,  # unreferenced local function has been removed
          4701,  # potentially uninitialized local variable 'sizew' used
          4706,  # assignment within conditional expression
          4804,  # unsafe use of type 'bool' in operation
          4996,  # this function or variable may be unsafe.
        ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'WarnAsError': 'false',
          },
        },
        'xcode_settings': {
          'GCC_TREAT_WARNINGS_AS_ERRORS': 'NO',
          'WARNING_CFLAGS': [
            '-Wno-parentheses-equality',
            '-Wno-unused-function',
            '-Wno-sometimes-uninitialized',
            '-Wno-pointer-sign',
            '-Wno-sign-compare',
            '-Wno-string-plus-int',
            '-Wno-unused-variable',
            '-Wno-deprecated-declarations',
            '-Wno-return-type',
            '-Wno-gnu-folding-constant',
          ],
        },
        'conditions': [
          ['OS=="linux"', {
            'cflags': [
              '-Wno-parentheses-equality',
              '-Wno-unused-function',
              '-Wno-sometimes-uninitialized',
              '-Wno-pointer-sign',
              '-Wno-string-plus-int',
              '-Wno-unused-variable',
              '-Wno-unused-value',
              '-Wno-deprecated-declarations',
              '-Wno-return-type',
              # Required when building as shared library.
              '-fPIC',
            ],
          }],
        ],
      }],
      ['_target_name=="node"', {
        'include_dirs': [ '<(libchromiumcontent_src_dir)/v8/include' ],
        'conditions': [
          ['OS=="mac" and libchromiumcontent_component==0', {
            'xcode_settings': {
              'OTHER_LDFLAGS': [ '-Wl,-all_load' ],
            },
          }],
          ['OS=="linux" and libchromiumcontent_component==0', {
            # Prevent the linker from stripping symbols.
            'ldflags': [
              '-Wl,--whole-archive',
              '<@(libchromiumcontent_v8_libraries)',
              '-Wl,--no-whole-archive',
            ],
          }, {
            'libraries': [ '<@(libchromiumcontent_v8_libraries)' ],
          }],
        ],
      }],
      ['_target_name=="libuv"', {
        'conditions': [
          ['OS=="win"', {
            # Expose libuv's symbols.
            'defines': [
              'BUILDING_UV_SHARED=1',
            ],
          }],  # OS=="win"
        ],
      }],
      ['_target_name.startswith("breakpad") or _target_name in ["crash_report_sender", "dump_syms"]', {
        'conditions': [
          ['OS=="mac"', {
            'xcode_settings': {
              'WARNING_CFLAGS': [
                '-Wno-deprecated-declarations',
                '-Wno-deprecated-register',
                '-Wno-unused-private-field',
                '-Wno-unused-function',
              ],
            },
          }],  # OS=="mac"
          ['OS=="linux"', {
            'cflags': [
              '-Wno-empty-body',
            ],
          }],  # OS=="linux"
          ['OS=="win"', {
            'msvs_disabled_warnings': [
              # unreferenced local function has been removed.
              4505,
            ],
          }],  # OS=="win"
        ],
      }],
    ],
    'msvs_cygwin_shell': 0, # Strangely setting it to 1 would make building under cygwin fail.
    'msvs_disabled_warnings': [
      4005,  # (node.h) macro redefinition
      4189,  # local variable is initialized but not referenced
      4201,  # (uv.h) nameless struct/union
      4503,  # decorated name length exceeded, name was truncated
      4800,  # (v8.h) forcing value to bool 'true' or 'false'
      4819,  # The file contains a character that cannot be represented in the current code page
      4996,  # (atlapp.h) 'GetVersionExW': was declared deprecated
    ],
  },
  'conditions': [
    # The breakdpad on Windows assumes Debug_x64 and Release_x64 configurations.
    ['OS=="win"', {
      'target_defaults': {
        'configurations': {
          'Debug_x64': {
          },
          'Release_x64': {
          },
        },
      },
    }],  # OS=="win"
    # The breakdpad on Mac assumes Release_Base configuration.
    ['OS=="mac"', {
      'target_defaults': {
        'configurations': {
          'Release_Base': {
          },
        },
      },
    }],  # OS=="mac"
  ],
}
