import cooler
import h5py
import numpy as np

def dump_bins_from_mcool(input_mcool_file, output_text_file, resolution_index_str=None, resolution_str=None):
      fo=open(output_text_file, 'a+')
      with h5py.File(input_mcool_file, 'r') as f:
          if 'resolutions' in f and resolution_str:
              single_cool = f['resolutions'][resolution_str]
          elif 'resolutions' not in f and resolution_index_str:
              single_cool = f[resolution_index_str]
          else:
              raise Exception("Newer version of cool needs resolution_str (e.g. '5000') and older version needs resolution index (e.g. '0')")
          c=cooler.Cooler(single_cool)
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
    parser.add_argument('-n','--nres', help='number of resolutions (for older version of mcool)')
    parser.add_argument('-u','--res_list', help='list of resolutions, comma-separated (for both older and newer versions of mcool)')
    args = parser.parse_args()
 
    input_mcool_file = args.input
    output_prefix = args.output_prefix

    # older version mcool
    if args.nres and not args.res_list:
        for resolution_index in range(0, int(args.nres)):
            output_text_file = output_prefix + '.' + str(resolution_index)
            dump_bins_from_mcool(input_mcool_file, output_text_file,  resolution_index_str = str(resolution_index))

    # newer version mcool
    if not args.nres and args.res_list:
        for i, resolution in enumerate(args.res_list.split(',')):
            output_text_file = output_prefix + '.' + str(i)
            dump_bins_from_mcool(input_mcool_file, output_text_file, resolution_index_str = str(i), resolution_str = resolution)


