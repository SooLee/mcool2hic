import cooler
import h5py
import numpy as np

def dump_bins_from_mcool(input_mcool_file, output_text_file, resolution_index_str):
      fo=open(output_text_file, 'a+')
      with h5py.File(input_mcool_file, 'r') as f:
          c=cooler.Cooler(f[resolution_index_str])
          selector = c.bins()
          n = c.info['nbins']
          chunksize = n
          # write in chunks
          edges = np.arange(0, n+chunksize, chunksize)
          edges[-1] = n
          for lo, hi in zip(edges[:-1], edges[1:]):
              sel = selector[lo:hi]
              sel.to_csv(fo, sep='\t', index=False, header=False, float_format='%g')



if __name__ == '__main__':

    import argparse
 
    parser = argparse.ArgumentParser(description = 'QC for Pairs')
    parser.add_argument('-i','--input', help = "input mcool file")
    parser.add_argument('-o','--output_prefix', help = "output_prefix")
    parser.add_argument('-n','--nres', help='number of resolutions')
    args = parser.parse_args()
 
    input_mcool_file = args.input
    output_prefix = args.output_prefix

    for resolution_index in range(0, int(args.nres)):
        output_text_file = output_prefix + '.' + str(resolution_index)
        dump_bins_from_mcool(input_mcool_file, output_text_file,  str(resolution_index))


