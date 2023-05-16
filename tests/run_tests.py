#!/usr/bin/env python
"""Execute the tests for the mason_variator program.

The golden test outputs are generated by the script generate_outputs.sh.

You have to give the root paths to the source and the binaries as arguments to
the program.  These are the paths to the directory that contains the 'projects'
directory.

Usage:  run_tests.py SOURCE_ROOT_PATH BINARY_ROOT_PATH
"""
import logging
import os.path
import sys

# Automagically add util/py_lib to PYTHONPATH environment variable.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'py_lib'))
sys.path.insert(0, path)

import seqan.app_tests as app_tests

def main(source_base, binary_base):
    """Main entry point of the script."""

    print('Executing test for mason_variator')
    print('======================')
    print()

    ph = app_tests.TestPathHelper(
        source_base, binary_base,
        'tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_genome = app_tests.autolocateBinary(
      binary_base, 'bin', 'mason_genome')
    path_to_methylation = app_tests.autolocateBinary(
      binary_base, 'bin', 'mason_methylation')
    path_to_variator = app_tests.autolocateBinary(
      binary_base, 'bin', 'mason_variator')
    path_to_materializer = app_tests.autolocateBinary(
      binary_base, 'bin', 'mason_materializer')
    path_to_simulator = app_tests.autolocateBinary(
      binary_base, 'bin', 'mason_simulator')

    libcpp = ('CC' in os.environ and 'gcc' in os.environ["CC"]) or sys.platform == "linux" or sys.platform == "linux2"

    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # We prepare a list of transforms to apply to the output files.  This is
    # used to strip the input/output paths from the programs' output to
    # make it more canonical and host independent.
    ph.outFile('-')  # To ensure that the out path is set.
    transforms = [
        app_tests.ReplaceTransform(
            os.path.join(ph.source_base_path,
                         'tests') + os.sep,
            '', right=True),
        app_tests.ReplaceTransform(ph.temp_dir + os.sep, '', right=True),
        app_tests.NormalizeScientificExponentsTransform(),
        ]

    # ============================================================
    # Test mason_genome
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_genome,
        args=['-l', '1000',
              '-o', ph.outFile('genome.test1.fasta'),
              ],
        redir_stdout=ph.outFile('genome.test1.stdout'),
        redir_stderr=ph.outFile('genome.test1.stderr'),
        to_diff=[(ph.inFile('genome.test1.fasta'),
                  ph.outFile('genome.test1.fasta')),
                 (ph.inFile('genome.test1.stdout'),
                  ph.outFile('genome.test1.stdout'),
                  transforms),
                 (ph.inFile('genome.test1.stderr'),
                  ph.outFile('genome.test1.stderr'),
                  transforms),
                 ])
    conf_list.append(conf)
    conf = app_tests.TestConf(
        program=path_to_genome,
        args=['-s', '1',
              '-l', '1000',
              '-l', '100',
              '-o', ph.outFile('genome.test2.fasta'),
              ],
        redir_stdout=ph.outFile('genome.test2.stdout'),
        redir_stderr=ph.outFile('genome.test2.stderr'),
        to_diff=[(ph.inFile('genome.test2.fasta'),
                  ph.outFile('genome.test2.fasta')),
                 (ph.inFile('genome.test2.stdout'),
                  ph.outFile('genome.test2.stdout'),
                  transforms),
                 (ph.inFile('genome.test2.stderr'),
                  ph.outFile('genome.test2.stderr'),
                  transforms),
                 ])
    conf_list.append(conf)

    # ============================================================
    # Test mason_methylation
    # ============================================================

    conf = app_tests.TestConf(
        program=path_to_methylation,
        args=['--seed', '33',
              '-i', ph.inFile('random.fasta'),
              '-o', ph.outFile('random_meth1.fasta'),
              ],
        redir_stdout=ph.outFile('methylation.test1.stdout'),
        redir_stderr=ph.outFile('methylation.test1.stderr'),
        to_diff=[(ph.inFile('methylation.test1.fasta'),
                  ph.outFile('methylation.test1.fasta')),
                 (ph.inFile('methylation.test1.stdout'),
                  ph.outFile('methylation.test1.stdout'),
                  transforms),
                 (ph.inFile('methylation.test1.stderr'),
                  ph.outFile('methylation.test1.stderr'),
                  transforms),
                 ])

    # ============================================================
    # Test mason_variator
    # ============================================================

    # Generation methylation in variator.
    conf = app_tests.TestConf(
        program=path_to_variator,
        args=['-ir', ph.inFile('random.fasta'),
              '-n', '2',
              '-ov', ph.outFile('random_var1.vcf'),
              '-of', ph.outFile('random_var1.fasta'),
              '--snp-rate', '0.001',
              '--small-indel-rate', '0.001',
              '--sv-indel-rate', '0.001',
              '--sv-inversion-rate', '0.001',
              '--sv-translocation-rate', '0.001',
              '--sv-duplication-rate', '0.001',
              '--min-sv-size', '50',
              '--max-sv-size', '100',
              '--methylation-levels',
              '--meth-fasta-out', ph.outFile('random_var1_meth.fasta'),
              '--out-breakpoints', ph.outFile('random_var1_bp.txt'),
              ],
        redir_stdout=ph.outFile('random_var1.vcf.stdout'),
        redir_stderr=ph.outFile('random_var1.vcf.stderr'),
        to_diff=[(ph.inFile('random_var1.vcf'),
                  ph.outFile('random_var1.vcf'),
                  transforms),
                 (ph.inFile('random_var1.fasta'),
                  ph.outFile('random_var1.fasta')),
                 (ph.inFile('random_var1_bp.txt'),
                  ph.outFile('random_var1_bp.txt')),
                 (ph.inFile('random_var1_meth.fasta'),
                  ph.outFile('random_var1_meth.fasta')),
                 (ph.inFile('random_var1.vcf.stderr'),
                  ph.outFile('random_var1.vcf.stderr'),
                  transforms),
                 (ph.inFile('random_var1.vcf.stdout'),
                  ph.outFile('random_var1.vcf.stdout'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # Generation methylation in variator.
    conf = app_tests.TestConf(
        program=path_to_variator,
        args=['-ir', ph.inFile('random.fasta'),
              '-n', '2',
              '-ov', ph.outFile('random_var2.vcf'),
              '-of', ph.outFile('random_var2.fasta'),
              '--snp-rate', '0.001',
              '--small-indel-rate', '0.001',
              '--sv-indel-rate', '0.001',
              '--sv-inversion-rate', '0.001',
              '--sv-translocation-rate', '0.001',
              '--sv-duplication-rate', '0.001',
              '--min-sv-size', '50',
              '--max-sv-size', '100',
              '--methylation-levels',
              '--meth-fasta-in', ph.inFile('random_meth1.fasta'),
              '--meth-fasta-out', ph.outFile('random_var2_meth.fasta'),
              '--out-breakpoints', ph.outFile('random_var2_bp.txt'),
              ],
        redir_stdout=ph.outFile('random_var2.vcf.stdout'),
        redir_stderr=ph.outFile('random_var2.vcf.stderr'),
        to_diff=[(ph.inFile('random_var2.vcf'),
                  ph.outFile('random_var2.vcf'),
                  transforms),
                 (ph.inFile('random_var2.fasta'),
                  ph.outFile('random_var2.fasta')),
                 (ph.inFile('random_var2_bp.txt'),
                  ph.outFile('random_var2_bp.txt')),
                 (ph.inFile('random_var2_meth.fasta'),
                  ph.outFile('random_var2_meth.fasta')),
                 (ph.inFile('random_var2.vcf.stderr'),
                  ph.outFile('random_var2.vcf.stderr'),
                  transforms),
                 (ph.inFile('random_var2.vcf.stdout'),
                  ph.outFile('random_var2.vcf.stdout'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # Variation without methylation levels.
    conf = app_tests.TestConf(
        program=path_to_variator,
        args=['-ir', ph.inFile('random.fasta'),
              '-n', '2',
              '-ov', ph.outFile('random_var3.vcf'),
              '-of', ph.outFile('random_var3.fasta'),
              '--snp-rate', '0.001',
              '--small-indel-rate', '0.001',
              '--sv-indel-rate', '0.001',
              '--sv-inversion-rate', '0.001',
              '--sv-translocation-rate', '0.001',
              '--sv-duplication-rate', '0.001',
              '--min-sv-size', '50',
              '--max-sv-size', '100',
              '--out-breakpoints', ph.outFile('random_var3_bp.txt'),
              ],
        redir_stdout=ph.outFile('random_var3.vcf.stdout'),
        redir_stderr=ph.outFile('random_var3.vcf.stderr'),
        to_diff=[(ph.inFile('random_var3.vcf'),
                  ph.outFile('random_var3.vcf'),
                  transforms),
                 (ph.inFile('random_var3.fasta'),
                  ph.outFile('random_var3.fasta')),
                 (ph.inFile('random_var3_bp.txt'),
                  ph.outFile('random_var3_bp.txt')),
                 (ph.inFile('random_var3.vcf.stderr'),
                  ph.outFile('random_var3.vcf.stderr'),
                  transforms),
                 (ph.inFile('random_var3.vcf.stdout'),
                  ph.outFile('random_var3.vcf.stdout'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # Previously crashing test
    conf = app_tests.TestConf(
        program=path_to_variator,
        args=['-ir', ph.inFile('adeno_virus.fa'),
              '-ov', ph.outFile('random_var9.vcf'),
              '-of', ph.outFile('random_var9.fasta'),
              '--sv-indel-rate', '0.01',
              '--sv-duplication-rate', '0.01',
              '--sv-inversion-rate', '0.01',
              '--min-sv-size', '20',
              '--max-sv-size', '300',
              ],
        redir_stdout=ph.outFile('random_var9.vcf.stdout'),
        redir_stderr=ph.outFile('random_var9.vcf.stderr'),
        to_diff=[(ph.inFile('random_var9.vcf'),
                  ph.outFile('random_var9.vcf'),
                  transforms),
                 (ph.inFile('random_var9.vcf.stderr'),
                  ph.outFile('random_var9.vcf.stderr'),
                  transforms),
                 (ph.inFile('random_var9.vcf.stdout'),
                  ph.outFile('random_var9.vcf.stdout'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # ============================================================
    # Test mason_materializer
    # ============================================================

    # Without methylation levels.
    conf = app_tests.TestConf(
        program=path_to_materializer,
        args=['-ir', ph.inFile('random.fasta'),
              '-iv', ph.inFile('random_var1.vcf'),
              '-o', ph.outFile('materializer.random_var1.fasta'),
              ],
        redir_stdout=ph.outFile('materializer.random_var1.stdout'),
        redir_stderr=ph.outFile('materializer.random_var1.stderr'),
        to_diff=[(ph.inFile('random_var1.fasta'),
                  ph.outFile('materializer.random_var1.fasta')),
                 (ph.inFile('materializer.random_var1.stdout'),
                  ph.outFile('materializer.random_var1.stdout'),
                  transforms),
                 (ph.inFile('materializer.random_var1.stderr'),
                  ph.outFile('materializer.random_var1.stderr'),
                  transforms),
                 ])
    conf_list.append(conf)

    # With methylation levels.
    conf = app_tests.TestConf(
        program=path_to_materializer,
        args=['-ir', ph.inFile('random.fasta'),
              '-iv', ph.inFile('random_var2.vcf'),
              '-o', ph.outFile('materializer.random_var2.fasta'),
              '--meth-fasta-in', ph.inFile('random_meth1.fasta'),
              '--meth-fasta-out', ph.outFile('materializer.random_meth2.fasta'),
              ],
        redir_stdout=ph.outFile('materializer.random_var2.stdout'),
        redir_stderr=ph.outFile('materializer.random_var2.stderr'),
        to_diff=[(ph.inFile('random_var1.fasta'),
                  ph.outFile('materializer.random_var1.fasta')),
                 (ph.inFile('random_var2_meth.fasta'),
                  ph.outFile('materializer.random_meth2.fasta'),
                  transforms),
                 (ph.inFile('materializer.random_var2.stdout'),
                  ph.outFile('materializer.random_var2.stdout'),
                  transforms),
                 (ph.inFile('materializer.random_var2.stderr'),
                  ph.outFile('materializer.random_var2.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # ============================================================
    # Test mason_simulator
    # ============================================================

    # Illumina Model

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-o', ph.outFile('simulator.left1.fq'),
              '-or', ph.outFile('simulator.right1.fq'),
              '-oa', ph.outFile('simulator.out1.sam'),
              ],
        redir_stdout=ph.outFile('simulator.out1.stdout'),
        redir_stderr=ph.outFile('simulator.out1.stderr'),
        to_diff=[(ph.inFile('simulator.left1.fq'),
                  ph.outFile('simulator.left1.fq')),
                 (ph.inFile('simulator.right1.fq'),
                  ph.outFile('simulator.right1.fq')),
                 (ph.inFile('simulator.out1.sam'),
                  ph.outFile('simulator.out1.sam')),
                 (ph.inFile('simulator.out1.stdout'),
                  ph.outFile('simulator.out1.stdout'),
                  transforms),
                 (ph.inFile('simulator.out1.stderr'),
                  ph.outFile('simulator.out1.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-iv', ph.inFile('random_var1.vcf'),
              '-o', ph.outFile('simulator.left2.fq'),
              '-or', ph.outFile('simulator.right2.fq'),
              '-oa', ph.outFile('simulator.out2.sam'),
              ],
        redir_stdout=ph.outFile('simulator.out2.stdout'),
        redir_stderr=ph.outFile('simulator.out2.stderr'),
        to_diff=[(ph.inFile('simulator.left2.fq'),
                  ph.outFile('simulator.left2.fq')),
                 (ph.inFile('simulator.right2.fq'),
                  ph.outFile('simulator.right2.fq')),
                 (ph.inFile('simulator.out2.sam'),
                  ph.outFile('simulator.out2.sam')),
                 (ph.inFile('simulator.out2.stdout'),
                  ph.outFile('simulator.out2.stdout'),
                  transforms),
                 (ph.inFile('simulator.out2.stderr'),
                  ph.outFile('simulator.out2.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-o', ph.outFile('simulator.left3.fa'),
              '-or', ph.outFile('simulator.right3.fa'),
              ],
        redir_stdout=ph.outFile('simulator.out3.stdout'),
        redir_stderr=ph.outFile('simulator.out3.stderr'),
        to_diff=[(ph.inFile('simulator.left3.fa'),
                  ph.outFile('simulator.left3.fa')),
                 (ph.inFile('simulator.right3.fa'),
                  ph.outFile('simulator.right3.fa')),
                 (ph.inFile('simulator.out3.stdout'),
                  ph.outFile('simulator.out3.stdout'),
                  transforms),
                 (ph.inFile('simulator.out3.stderr'),
                  ph.outFile('simulator.out3.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-iv', ph.inFile('random_var1.vcf'),
              '-o', ph.outFile('simulator.left7.fa'),
              '-oa', ph.outFile('simulator.out7.sam'),
              ],
        redir_stdout=ph.outFile('simulator.out7.stdout'),
        redir_stderr=ph.outFile('simulator.out7.stderr'),
        to_diff=[(ph.inFile('simulator.left7.fa'),
                  ph.outFile('simulator.left7.fa')),
                 (ph.inFile('simulator.out7.sam'),
                  ph.outFile('simulator.out7.sam')),
                 (ph.inFile('simulator.out7.stdout'),
                  ph.outFile('simulator.out7.stdout'),
                  transforms),
                 (ph.inFile('simulator.out7.stderr'),
                  ph.outFile('simulator.out7.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-o', ph.outFile('simulator.left4.fa'),
              '-oa', ph.outFile('simulator.out4.sam'),
              ],
        redir_stdout=ph.outFile('simulator.out4.stdout'),
        redir_stderr=ph.outFile('simulator.out4.stderr'),
        to_diff=[(ph.inFile('simulator.left4.fa'),
                  ph.outFile('simulator.left4.fa')),
                 (ph.inFile('simulator.out4.sam'),
                  ph.outFile('simulator.out4.sam')),
                 (ph.inFile('simulator.out4.stdout'),
                  ph.outFile('simulator.out4.stdout'),
                  transforms),
                 (ph.inFile('simulator.out4.stderr'),
                  ph.outFile('simulator.out4.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '--meth-fasta-in', ph.inFile('random_meth1.fasta'),
              '--methylation-levels',
              '--enable-bs-seq',
              '-o', ph.outFile('simulator.left5.fq'),
              '-or', ph.outFile('simulator.right5.fq'),
              ],
        redir_stdout=ph.outFile('simulator.out5.stdout'),
        redir_stderr=ph.outFile('simulator.out5.stderr'),
        to_diff=[(ph.inFile('simulator.left5.fq'),
                  ph.outFile('simulator.left5.fq')),
                 (ph.inFile('simulator.right5.fq'),
                  ph.outFile('simulator.right5.fq')),
                 (ph.inFile('simulator.out5.stdout'),
                  ph.outFile('simulator.out5.stdout'),
                  transforms),
                 (ph.inFile('simulator.out5.stderr'),
                  ph.outFile('simulator.out5.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['-n', '1000',
              '-ir', ph.inFile('random.fasta'),
              '-iv', ph.inFile('random_var1.vcf'),
              '--meth-fasta-in', ph.inFile('random_meth1.fasta'),
              '--methylation-levels',
              '--enable-bs-seq',
              '-o', ph.outFile('simulator.left6.fq'),
              '-or', ph.outFile('simulator.right6.fq'),
              ],
        redir_stdout=ph.outFile('simulator.out6.stdout'),
        redir_stderr=ph.outFile('simulator.out6.stderr'),
        to_diff=[(ph.inFile('simulator.left6.fq'),
                  ph.outFile('simulator.left6.fq')),
                 (ph.inFile('simulator.right6.fq'),
                  ph.outFile('simulator.right6.fq')),
                 (ph.inFile('simulator.out6.stdout'),
                  ph.outFile('simulator.out6.stdout'),
                  transforms),
                 (ph.inFile('simulator.out6.stderr'),
                  ph.outFile('simulator.out6.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # 454 Model

    conf = app_tests.TestConf(
        program=path_to_simulator,
        args=['--seq-technology', '454',
              '--fragment-mean-size', '800',
              '--454-read-length-mean', '200',
              '--454-read-length-stddev', '20',
              '-n', '1000', '-v',
              '-ir', ph.inFile('random.fasta'),
              '-o', ph.outFile('simulator.left8.fq'),
              '-oa', ph.outFile('simulator.out8.sam'),
              ],
        redir_stdout=ph.outFile('simulator.out8.stdout'),
        redir_stderr=ph.outFile('simulator.out8.stderr'),
        to_diff=[(ph.inFile('simulator.left8.fq'),
                  ph.outFile('simulator.left8.fq')),
                 (ph.inFile('simulator.out8.sam'),
                  ph.outFile('simulator.out8.sam')),
                 (ph.inFile('simulator.out8.stdout'),
                  ph.outFile('simulator.out8.stdout'),
                  transforms),
                 (ph.inFile('simulator.out8.stderr'),
                  ph.outFile('simulator.out8.stderr'),
                  transforms),
                 ])
    if libcpp:
        conf_list.append(conf)

    # Execute the tests.
    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print(' '.join([os.path.basename(conf.program)] + conf.args), end=' ')
        if res:
             print('OK')
        else:
            failures += 1
            print('FAILED')

    # Cleanup.
    ph.deleteTempDir()

    print('==============================')
    print('     total tests: %d' % len(conf_list))
    print('    failed tests: %d' % failures)
    print('successful tests: %d' % (len(conf_list) - failures))
    print('==============================')
    # Compute and return return code.
    return failures != 0


if __name__ == '__main__':
    sys.exit(app_tests.main(main))
