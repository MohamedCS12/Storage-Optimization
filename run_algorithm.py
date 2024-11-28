from py3dbp import Packer, Bin, Item, Painter

def run_packing_algorithm(items, container_list):
    packer = Packer()


    # Add all containers to the packer
    for container_details in container_list:
        container_name, container_dimensions, max_weight = container_details
        container_length, container_width, container_height = container_dimensions
        box = Bin(container_name, (container_length, container_width, container_height), max_weight)
        packer.addBin(box)

    # Add all items to the packer
    for item_details in items:
        partno, (length, width, height), weight, level, loadbear, updown, color = item_details
        item = Item(partno=partno, name='test', typeof='cube', WHD=(length, width, height), weight=weight, level=level, loadbear=loadbear, updown=updown, color=color)
        packer.addItem(item)

    # Perform packing operation with correct parameters
    packer.pack(
        bigger_first=True,                  # Sort items and bins by size (biggest first)
        distribute_items=True,              # Distribute items across multiple containers
        fix_point=True,                     # Fix the position of items
        check_stable=True,                  # Check stability of items in the bin
        support_surface_ratio=0.75,         # Minimum surface support ratio
        binding=[],                         # No specific binding or grouping
        number_of_decimals=0                # Set decimal precision for item dimensions
    )

    packer.putOrder()

    # Prepare results
    results = []
    for b in packer.bins:
        bin_result = {
            'fitted_items': [],
            'unfitted_items': [],
            'volume': b.getVolume(),
            'volume_fitted': 0,
            'volume_unfitted': 0,
            'space_utilization': 0,
            'gravity_distribution': b.gravity
        }

        # Add fitted items to the bin result
        for item in b.items:
            fitted_item = {
                'partno': item.partno,
                'dimensions': (item.width, item.height, item.depth),
                'weight': item.weight,
                'position': item.position,
                'rotation_type': item.rotation_type
            }
            bin_result['fitted_items'].append(fitted_item)
            bin_result['volume_fitted'] += item.width * item.height * item.depth

        # Add unfitted items to the bin result
        for item in packer.unfit_items:
            unfitted_item = {
                'partno': item.partno,
                'dimensions': (item.width, item.height, item.depth),
                'weight': item.weight
            }
            bin_result['unfitted_items'].append(unfitted_item)
            bin_result['volume_unfitted'] += item.width * item.height * item.depth

        # draw results
        painter = Painter(b)
        fig = painter.plotBoxAndItems(
            title=b.partno,
            alpha=0.8,
            write_num=False,
            fontsize=10
        )
        
        # Calculate space utilization
        bin_result['space_utilization'] = round(bin_result['volume_fitted'] / bin_result['volume'] * 100, 2) if bin_result['volume'] > 0 else 0
        results.append(bin_result)

        fig.show()

    
    return results