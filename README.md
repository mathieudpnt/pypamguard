# PyPAMGuard
Python module for reading passive acoustic binary data files created by the program PAMGuard (https://www.pamguard.org/).

## File Structure

PAMGuard outputs binary data files (.pgdf) which offer significant efficiencies over other slower storage mechanisms. The tradeoff is that these files are not human readable and require some middleware to interpret. That is what this library does.

A `PAMFile` is split into a number of PAMChunks. PAMChunks are not all equal in type - for example the fileHeader and genericModule chunks will differ from each other. Each `PAMChunk` contains information about its `length`, an `identifier` and a number of attributes that are specific to that particular subclass of `PAMChunk`.