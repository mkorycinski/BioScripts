"""
Script for parsing HMMER3 output text format into JSON format.
"""

import json
import argparse
from os import sys
from Bio import SearchIO


def parse_user_arguments(argv):
    """Parse user arguments to ease the use of the script"""

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=
                                     argparse.RawTextHelpFormatter)

    parser.add_argument('-i',
                        '--input-file',
                        help='HMMER3 text output file',
                        type=str,
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        help='JSON output file',
                        type=str,
                        required=False)

    arguments = parser.parse_args(argv)

    return arguments


def hit2dict(hit):
    """
    Turns biopythons' Hit object into dictionary
    that can be easily serialized by json.
    
    :param hit: Bio.SearchIO._model.Hit object
    :return: dictionary representation of an object
    """
    
    hit_json = {
        'description': hit.description,
        'bias': hit.bias,
        'bitscore': hit.bitscore,
        'evalue': hit.evalue,
        'dom_exp_num': hit.domain_exp_num,
        'domain_obs_num': hit.domain_obs_num
    }
    
    return hit_json


def hsp2dict(hsp):
    """
    Turns biopythons' HSP object into dictionary
    that can be easily serialized by json.
    
    :param hsp: Bio.SearchIO._model.HSP
    :return:
    """
    
    hsp_json = {
        'bias': hsp.bias,
        'bitscore': hsp.bitscore,
        'evalue': hsp.evalue,
        'acc_avg': hsp.acc_avg,
        'env_start': hsp.env_start,
        'env_end': hsp.env_end,
        'query_id': hsp.query.id,
        'query_description': hsp.query.description,
        'query_seq': str(hsp.query.seq),
        'query_start': hsp.query_start,
        'query_end': hsp.query_end,
        'hit_id': hsp.hit.id,
        'hit_description': hsp.hit.description,
        'hit_seq': str(hsp.hit.seq),
        'hit_start': hsp.hit_start,
        'hit_end': hsp.hit_end,
    }
    
    return hsp_json


def hmmer2json(in_file):
    """
    Reads hmmer results with biopython and turns
    it into data that can be serialized with json.
    
    :param in_file: Input file with hmmer results
    :return: json dict
    """
    
    # This is how json output will be structured
    results = {'id': '',
               'description': '',
               'hits': [],
               'hsps': [],
               }
    
    with open(in_file, 'r') as handle:
        for qres in SearchIO.parse(handle=handle,
                                   format='hmmer3-text'):
            results['id'] = qres.id
            results['description'] = qres.description
            for hit in qres.hits:
                results['hits'].append(hit2dict(hit))
            for hsp in qres.hsps:
                results['hsps'].append(hsp2dict(hsp))
                
    return results


def main(args):

    if not args.output_file:
        args.output_file = '%s.json' % \
                           args.input_file[:args.input_file.rfind('.')]
    
    json_data = hmmer2json(args.input_file)
    
    with open(args.output_file, 'w') as handle:
        json.dump(json_data, handle)
    
    
if __name__ == '__main__':
    args = parse_user_arguments(sys.argv[1:])
    main(args)
