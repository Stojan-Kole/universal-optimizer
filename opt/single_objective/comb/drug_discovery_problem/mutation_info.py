from typing import Dict, List, Tuple

class MutationInfo:
    """
    Loads mutation rules for atoms, groups, and insertions from predefined text files.
    
    These rules are later used by the genetic algorithm for mutating molecular structures.
    """
    def __init__(self) -> None:
        """
        Initializes mutation data by reading from:
        - atom_switch.txt: rules for atom substitutions with weights
        - group_switch.txt: rules for functional group substitutions
        - insertion.txt: insertable groups or atoms
        """
        self.atom_switch_map: Dict[str, List[Tuple[str, float]]] = {}
        with open('opt/single_objective/comb/drug_discovery_problem/mutations/atom_switch.txt', 'r') as atom_switch_file:
            for line in atom_switch_file:
                line = line.strip()
                parts = line.split(' ')
                if parts[0] not in self.atom_switch_map:
                    self.atom_switch_map[parts[0]] = []
                self.atom_switch_map[parts[0]].append((parts[1], float(parts[2])))

        self.group_switch_map: Dict[str, List[str]] = {}
        with open('opt/single_objective/comb/drug_discovery_problem/mutations/group_switch.txt', 'r') as group_switch_file:
            for line in group_switch_file:
                line = line.strip()
                parts = line.split()
                if parts[0] not in self.group_switch_map:
                    self.group_switch_map[parts[0]] = []
                self.group_switch_map[parts[0]].append(parts[1])

        self.insertions: List[str] = []
        with open('opt/single_objective/comb/drug_discovery_problem/mutations/insertion.txt', 'r') as insertion_file:
            for line in insertion_file:
                line = line.strip()
                self.insertions.append(line)