import os
from nexus.writer import NexusWriter
from nexus.tools.check_for_valid_NexusReader import check_for_valid_NexusReader

def combine_nexuses(nexuslist):
    """
    Combines a list of NexusReader instances into a single nexus

    :param nexuslist: A list of NexusReader instances
    :type nexuslist: List

    :return: A NexusWriter instance

    :raises TypeError: if nexuslist is not a list of NexusReader instances
    :raises IOError: if unable to read an file in nexuslist
    :raises NexusFormatException: if a nexus file does not have a `data` block
    """
    out = NexusWriter()
    # check they're all nexus instances and get all block types
    blocks = set()
    for nex in nexuslist:
        check_for_valid_NexusReader(nex)
        blocks.update(list(nex.blocks))
    
    for block in blocks:
        if block == 'data':
            out = combine_datablocks(out, nexuslist)
        elif block == 'trees':
            out = combine_treeblocks(out, nexuslist)
        else:
            raise ValueError("Don't know how to combine %s blocks" % block)
    return out


def combine_treeblocks(out, nexuslist):
    for nex in nexuslist:
        check_for_valid_NexusReader(nex, required_blocks=['trees'])
        out.trees.extend(nex.trees.trees)
    return out


def combine_datablocks(out, nexuslist):
    charpos = 0
    for nex_id, nex in enumerate(nexuslist, 1):
        check_for_valid_NexusReader(nex, required_blocks=['data'])
        if hasattr(nex, 'short_filename'):
            nexus_label = os.path.splitext(nex.short_filename)[0]
        else:
            nexus_label = str(nex_id)
        
        out.add_comment(
            "%d - %d: %s" %
            (charpos, charpos + nex.data.nchar - 1, nexus_label)
        )
        
        # handle data
        for site_idx, site in enumerate(sorted(nex.data.characters), 0):
            data = nex.data.characters.get(site)
            charpos += 1
            # work out character label
            charlabel = nex.data.charlabels.get(site_idx, site_idx + 1)
            label = '%s.%s' % (nexus_label, charlabel)

            for taxon, value in data.items():
                out.add(taxon, label, value)
    return out
    