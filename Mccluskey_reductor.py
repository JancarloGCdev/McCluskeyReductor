# -*- coding: utf-8 -*-
#Paso 1----------------
minterms_list = [int(minterm) for minterm in input("Enter the minterms: ").strip().split(',')]
minterms_list.sort()
number_of_variables = len(bin(minterms_list[-1])) - 2

print(f"La lista de minterminos tiene máximo {number_of_variables} variables")

mccluskey_implicants_dict = {}
binary_minterms_groups = {}
all_implicants = set()

for minterm in minterms_list:
    try:
        binary_minterms_groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(number_of_variables))
    except KeyError:
        binary_minterms_groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(number_of_variables)]

#PARTE 2-------

def single_bit_change_validate(combiner,to_combine): # Function for checking if 2 minterms differ by 1 bit only
    bit_change_counter = 0
    for i in range(len(combiner)):
        if combiner[i] != to_combine[i]:
            bit_position_changed = i
            bit_change_counter += 1
            if bit_change_counter>1:
                return (False,None)
    return (True,bit_position_changed)

def flatten_list_minterms_group(minterms_group): # Flattens a list
    flattened_items = []
    for key_group in minterms_group:
        flattened_items.extend(minterms_group[key_group])
    return flattened_items



def findminterms(a): #Function for finding out which minterms are merged. For example, 10-1 is obtained by merging 9(1001) and 11(1011)
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
    temp = []
    for i in range(pow(2,gaps)):
        temp2,ind = a[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+temp2[ind+1:].find('-')+1
            else:
                ind = temp2[ind+1:].find('-')
            temp2 = temp2[:ind]+j+temp2[ind+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp


while True:
    temporal_minterms_group = binary_minterms_groups.copy()
    binary_minterms_groups,new_group_key,marked_minterms,should_stop = {},0,set(),True

    key_list = sorted(list(temporal_minterms_group.keys()))

    for i in range(len(key_list)-1):
        for combiner_minterm in temporal_minterms_group[key_list[i]]: # Loop which iterates through current group elements
            for minterm_to_combine in temporal_minterms_group[key_list[i+1]]: # Loop which iterates through next group elements
                single_bit_change = single_bit_change_validate(combiner_minterm,minterm_to_combine) # Compare the minterms   #MIRA QUE CAMBIE SOLO 1 BIT
                if single_bit_change[0]: # If the minterms differ by 1 bit only
                    try:
                        binary_minterms_groups[new_group_key].append(combiner_minterm[:single_bit_change[1]]+'-'+combiner_minterm[single_bit_change[1]+1:]) if combiner_minterm[:single_bit_change[1]]+'-'+combiner_minterm[single_bit_change[1]+1:] not in binary_minterms_groups[new_group_key] else None # LO GUARDA YA COMPARADO EN LA LLAVE M, M ES LA KEY DEL GRUPO DE LA SGTE ITERACION Put a '-' in the changing bit and add it to corresponding group
                    except KeyError:
                        binary_minterms_groups[new_group_key] = [combiner_minterm[:single_bit_change[1]]+'-'+combiner_minterm[single_bit_change[1]+1:]] # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                    should_stop = False
                    marked_minterms.add(combiner_minterm) # Mark element minterm combiner
                    marked_minterms.add(minterm_to_combine) # Mark element minterm to combine
        new_group_key += 1

    iteration_minterms_unmarked = set(flatten_list_minterms_group(temporal_minterms_group)).difference(marked_minterms) # Unmarked elements of each table
    all_implicants = all_implicants.union(iteration_minterms_unmarked) # Adding Prime Implicants to global list
    print("Unmarked elements(Prime Implicants) of this table:",None if len(iteration_minterms_unmarked)==0 else ', '.join(iteration_minterms_unmarked)) # Printing Prime Implicants of current table
    if should_stop: # If the minterms cannot be combined further
        print("\n\nAll Prime Implicants: ",None if len(all_implicants)==0 else ', '.join(all_implicants))
        for implicant in all_implicants:        # Print all prime implicants
            print(f"{implicant} : {findminterms(implicant)}")
        break

#Parte 3----- Tabla de comprobación y eliminación de minterms no necesarios
def remove_key_dict(to_delete, dict_delete):
  for a in to_delete:
    try:
      del dict_delete[a]
    except KeyError:
      None
  return dict_delete

def findVariables(x): # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list

final_implicants = []

for i in all_implicants:
    merged_minterms = findminterms(i)
    for j in merged_minterms:
        try:
            mccluskey_implicants_dict[j].append(i) if i not in mccluskey_implicants_dict[j] else None # Add minterm in chart
        except KeyError:
            mccluskey_implicants_dict[j] = [i]

temporal_implicants = mccluskey_implicants_dict.copy()
to_delete = []

for column_key in mccluskey_implicants_dict:
  if(len(mccluskey_implicants_dict[column_key]) == 1):
    final_implicants.append(mccluskey_implicants_dict[column_key][0]) if mccluskey_implicants_dict[column_key][0] not in final_implicants else None
    del temporal_implicants[column_key]
    for key in temporal_implicants:
      for imp in temporal_implicants[key]:
        if(imp == mccluskey_implicants_dict[column_key][0]):
          to_delete.append(key)


temporal_implicants = remove_key_dict(to_delete, temporal_implicants)

row_implicants = {}

for key in temporal_implicants:
  for x_implicant in temporal_implicants[key]:
    try:
      row_implicants[x_implicant].append(key)
    except KeyError:
      row_implicants[x_implicant] = [key]

to_delete = []

while bool(row_implicants):
  ultima_copia = row_implicants.copy()
  mayor = 0
  for i in ultima_copia:
    if(len(ultima_copia[i]) > mayor ):
      mayor = len(ultima_copia[i])
      key_mayor = i

  lista_a_borrar = row_implicants[key_mayor]
  final_implicants.append(key_mayor) if key_mayor not in final_implicants else None
  del row_implicants[key_mayor]

  for key in row_implicants:
    for i in lista_a_borrar:
      try:
        row_implicants[key].remove(i)
      except ValueError:
        None
    if(len(row_implicants[key]) == 0):
      to_delete.append(key)

  row_implicants = remove_key_dict(to_delete, row_implicants)


print_implicants = []
for i in final_implicants:
  print_implicants.append(findVariables(i))

if(print_implicants[0] != []):
  print(f"Estos son todos los implicantes: \n {all_implicants}")
  print('\n\nSolution: F = '+' + '.join(''.join(i) for i in print_implicants))
else:
  print('\n\nSolution: F = 1')