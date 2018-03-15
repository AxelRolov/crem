__author__ = 'Pavel Polishchuk'

import argparse
import sys
sys.path.insert(0, '/home/pavlop/python/crem')
from mutate import mutate_mol

from rdkit import Chem
from rdkit.Chem.Descriptors import MolWt


def main(input_smiles, id, iteration, job_id, db_name, output_fname, ncpu):
    m = Chem.AddHs(Chem.MolFromSmiles(input_smiles))
    iterator = mutate_mol(m, db_name, radius=1, min_freq=10,
                          min_size=0, max_size=8,
                          min_rel_size=0, max_rel_size=0.5, min_inc=-1,
                          max_inc=1, replace_cycles=False, ncores=ncpu)
    with open(output_fname, 'wt') as f:
        f.write('\t'.join(['SMILES', 'ID', 'Parent', 'Iteration', "MW", 'transformation']) + '\n')
        for i, (smi, rxn) in enumerate(iterator):
            f.write('\t'.join((smi,
                               '%s-%s-%i' % (iteration, job_id, i),
                               id,
                               iteration,
                               str(round(MolWt(Chem.MolFromSmiles(smi)))),
                               rxn)) + '\n')
        f.flush()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Mutation of a single molecule.')
    parser.add_argument('-i', '--input', metavar='input_smiles', required=True,
                        help='input one SMILES string.')
    parser.add_argument('--id', metavar='id', required=True,
                        help='id of input SMILES.')
    parser.add_argument('--iteration', metavar='iteration_number', required=True,
                        help='iteration number.')
    parser.add_argument('--job_id', metavar='job_number', required=True,
                        help='job number.')
    parser.add_argument('-d', '--db_name', metavar='job_number', required=True,
                        help='job number.')
    parser.add_argument('-o', '--out', metavar='output.txt', required=True,
                        help='generated molecules.')
    parser.add_argument('-c', '--ncpu', metavar='NUMBER', required=False, default=1,
                        help='number of cpus used for computation. Default: 1.')
    # parser.add_argument('-v', '--verbose', action='store_true', default=False,
    #                     help='print progress.')

    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "input": input_smiles = v
        if o == "out": output_fname = v
        if o == "id": id = v
        if o == "ncpu": ncpu = int(v)
        if o == "iteration": iteration = v
        if o == "job_id": job_id = v
        if o == "db_name": db_name = v

    main(input_smiles=input_smiles,
         output_fname=output_fname,
         ncpu=ncpu,
         id=id,
         iteration=iteration,
         job_id=job_id,
         db_name=db_name)
