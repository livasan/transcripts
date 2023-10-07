def merge_elements(arr):
    merged_arr = []
    current_merged_element = ''

    for element in arr:
        if not element.startswith('DEAR ABBY:'):
            current_merged_element += ' ' + element
        else:
            if current_merged_element:
                merged_arr.append(current_merged_element.strip())
                current_merged_element = ''
            merged_arr.append(element)

        if current_merged_element:
            merged_arr[-1] += current_merged_element.strip()

    return merged_arr