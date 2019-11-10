import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;

public class Assignment5 {
	public static interface ValuePairFilter {
		public boolean filter(String x, String y);
	}

	public static class DifferentValuesFilter implements ValuePairFilter {
		@Override
		public boolean filter(String x, String y) {
			return !x.equals(y);
		}
	}

	@SuppressWarnings("serial")
	public static class VariablesToDomainsMapping extends HashMap<String, ArrayList<String>> {
	}

	public static class CSP {
		@SuppressWarnings("unchecked")
		private VariablesToDomainsMapping deepCopyAssignment(VariablesToDomainsMapping assignment) {
			VariablesToDomainsMapping copy = new VariablesToDomainsMapping();
			for (String key : assignment.keySet()) {
				copy.put(key, (ArrayList<String>) assignment.get(key).clone());
			}
			return copy;
		}

		public class Pair<T> {
			public T x, y;

			public Pair(T x, T y) {
				this.x = x;
				this.y = y;
			}

			@Override
			public String toString() {
				return "(" + this.x + "," + this.y + ")";
			}
		}

		ArrayList<String> variables;
		VariablesToDomainsMapping domains;
		HashMap<String, HashMap<String, ArrayList<Pair<String>>>> constraints;

		public CSP() {
			// this.variables is a list of the variable names in the CSP
			this.variables = new ArrayList<String>();

			// this.domains.get(i) is a list of legal values for variable i
			this.domains = new VariablesToDomainsMapping();

			// this.constraints.get(i).get(j) is a list of legal value pairs for
			// the variable pair (i, j)
			this.constraints = new HashMap<String, HashMap<String, ArrayList<Pair<String>>>>();
		}

		/**
		 * Add a new variable to the CSP. 'name' is the variable name and
		 * 'domain' is a list of the legal values for the variable.
		 */
		@SuppressWarnings("unchecked")
		public void addVariable(String name, ArrayList<String> domain) {
			this.variables.add(name);
			this.domains.put(name, (ArrayList<String>) domain.clone());
			this.constraints.put(name, new HashMap<String, ArrayList<Pair<String>>>());
		}

		/**
		 * Get a list of all possible pairs (as tuples) of the values in the
		 * lists 'a' and 'b', where the first component comes from list 'a' and
		 * the second component comes from list 'b'.
		 */
		public ArrayList<Pair<String>> getAllPossiblePairs(ArrayList<String> a, ArrayList<String> b) {
			ArrayList<Pair<String>> pairs = new ArrayList<Pair<String>>();
			for (String x : a) {
				for (String y : b) {
					pairs.add(new Pair<String>(x, y));
				}
			}
			return pairs;
		}

		/**
		 * Get a list of all arcs/constraints that have been defined in the CSP.
		 * The arcs/constraints are represented as tuples of (i, j), indicating
		 * a constraint between variable 'i' and 'j'.
		 */
		public ArrayList<Pair<String>> getAllArcs() {
			ArrayList<Pair<String>> arcs = new ArrayList<Pair<String>>();
			for (String i : this.constraints.keySet()) {
				for (String j : this.constraints.get(i).keySet()) {
					arcs.add(new Pair<String>(i, j));
				}
			}
			return arcs;
		}

		/**
		 * Get a list of all arcs/constraints going to/from variable 'var'. The
		 * arcs/constraints are represented as in getAllArcs().
		 */
		public ArrayList<Pair<String>> getAllNeighboringArcs(String var) {
			ArrayList<Pair<String>> arcs = new ArrayList<Pair<String>>();
			for (String i : this.constraints.get(var).keySet()) {
				arcs.add(new Pair<String>(i, var));
			}
			return arcs;
		}

		/**
		 * Add a new constraint between variables 'i' and 'j'. The legal values
		 * are specified by supplying a function 'filterFunction', that returns
		 * true for legal value pairs and false for illegal value pairs. This
		 * function only adds the constraint one way, from i -> j. You must
		 * ensure that the function also gets called to add the constraint the
		 * other way, j -> i, as all constraints are supposed to be two-way
		 * connections!
		 */
		public void addConstraintOneWay(String i, String j, ValuePairFilter filterFunction) {
			if (!this.constraints.get(i).containsKey(j)) {
				this.constraints.get(i).put(j,
					this.getAllPossiblePairs(this.domains.get(i), this.domains.get(j)));
			}

			for (Iterator<Pair<String>> iter = this.constraints.get(i).get(j).iterator(); iter.hasNext();) {
				Pair<String> valuePair = iter.next();
				if (filterFunction.filter(valuePair.x, valuePair.y) == false) {
					iter.remove();
				}
			}
		}

		/**
		 * Add an Alldiff constraint between all of the variables in the list
		 * 'variables'.
		 */
		public void addAllDifferentConstraint(ArrayList<String> variables) {
			for (String i : variables) {
				for (String j : variables) {
					if (!i.equals(j)) {
						this.addConstraintOneWay(i, j, new DifferentValuesFilter());
					}
				}
			}
		}

		/**
		 * This functions starts the CSP solver and returns the found solution.
		 */
		public VariablesToDomainsMapping backtrackingSearch() {
			// Make a so-called "deep copy" of the dictionary containing the
			// domains of the CSP variables. The deep copy is required to
			// ensure that any changes made to 'assignment' does not have any
			// side effects elsewhere.
			VariablesToDomainsMapping assignment = this.deepCopyAssignment(this.domains);

			// Run AC-3 on all constraints in the CSP, to weed out all of the
			// values that are not arc-consistent to begin with
			this.inference(assignment, this.getAllArcs());

			// Call backtrack with the partial assignment 'assignment'
			return this.backtrack(assignment);
		}

		/**
		 * The function 'Backtrack' from the pseudocode in the textbook.
		 * 
		 * The function is called recursively, with a partial assignment of
		 * values 'assignment'. 'assignment' is a dictionary that contains a
		 * list of all legal values for the variables that have *not* yet been
		 * decided, and a list of only a single value for the variables that
		 * *have* been decided.
		 * 
		 * When all of the variables in 'assignment' have lists of length one,
		 * i.e. when all variables have been assigned a value, the function
		 * should return 'assignment'. Otherwise, the search should continue.
		 * When the function 'inference' is called to run the AC-3 algorithm,
		 * the lists of legal values in 'assignment' should get reduced as AC-3
		 * discovers illegal values.
		 * 
		 * IMPORTANT: For every iteration of the for-loop in the pseudocode, you
		 * need to make a deep copy of 'assignment' into a new variable before
		 * changing it. Every iteration of the for-loop should have a clean
		 * slate and not see any traces of the old assignments and inferences
		 * that took place in previous iterations of the loop.
		 */
		public VariablesToDomainsMapping backtrack(VariablesToDomainsMapping assignment) {
			// TODO: IMPLEMENT THIS
			return assignment;
		}

		/**
		 * The function 'Select-Unassigned-Variable' from the pseudocode in the
		 * textbook. Should return the name of one of the variables in
		 * 'assignment' that have not yet been decided, i.e. whose list of legal
		 * values has a length greater than one.
		 */
		public String selectUnassignedVariable(VariablesToDomainsMapping assignment) {
			// TODO: IMPLEMENT THIS
			return "";
		}

		/**
		 * The function 'AC-3' from the pseudocode in the textbook. 'assignment'
		 * is the current partial assignment, that contains the lists of legal
		 * values for each undecided variable. 'queue' is the initial queue of
		 * arcs that should be visited.
		 */
		public boolean inference(VariablesToDomainsMapping assignment, ArrayList<Pair<String>> queue) {
			// TODO: IMPLEMENT THIS
			return false;
		}

		/**
		 * The function 'Revise' from the pseudocode in the textbook.
		 * 'assignment' is the current partial assignment, that contains the
		 * lists of legal values for each undecided variable. 'i' and 'j'
		 * specifies the arc that should be visited. If a value is found in
		 * variable i's domain that doesn't satisfy the constraint between i and
		 * j, the value should be deleted from i's list of legal values in
		 * 'assignment'.
		 */
		public boolean revise(VariablesToDomainsMapping assignment, String i, String j) {
			// TODO: IMPLEMENT THIS
			return false;
		}
	}

	/**
	 * Instantiate a CSP representing the map coloring problem from the
	 * textbook. This can be useful for testing your CSP solver as you develop
	 * your code.
	 */
	public static CSP createMapColoringCSP() {
		CSP csp = new CSP();
		String states[] = { "WA", "NT", "Q", "NSW", "V", "SA", "T" };
		ArrayList<String> colors = new ArrayList<String>();
		colors.add("red");
		colors.add("green");
		colors.add("blue");
		for (String state : states) {
			csp.addVariable(state, colors);
		}
		for (String state : states) {
			ArrayList<String> neighbors = new ArrayList<String>();
			if (state.equals("SA")) {
				neighbors.add("WA");
				neighbors.add("NT");
				neighbors.add("Q");
				neighbors.add("NSW");
				neighbors.add("V");
			} else if (state.equals("NT")) {
				neighbors.add("WA");
				neighbors.add("Q");
			} else if (state.equals("NSW")) {
				neighbors.add("Q");
				neighbors.add("V");
			}

			for (String neighbor : neighbors) {
				csp.addConstraintOneWay(state, neighbor, new DifferentValuesFilter());
				csp.addConstraintOneWay(neighbor, state, new DifferentValuesFilter());
			}
		}
		return csp;
	}

	/**
	 * Instantiate a CSP representing the Sudoku board found in the text file
	 * named 'fileName' in the current directory.
	 */
	public static CSP createSudokuCSP(String fileName) {
		CSP csp = new CSP();
		Scanner scanner;
		try {
			scanner = new Scanner(new FileReader(fileName));
		} catch (FileNotFoundException e) {
			System.err.println("File not found " + fileName);
			return null;
		}
		ArrayList<String> domain = new ArrayList<String>();
		for (int i = 1; i <= 9; i++) {
			domain.add(i + "");
		}
		for (int row = 0; row < 9; row++) {
			String boardRow = scanner.nextLine();
			for (int col = 0; col < 9; col++) {
				if (boardRow.charAt(col) == '0') {
					csp.addVariable(row + "-" + col, domain);
				} else {
					ArrayList<String> currentDomain = new ArrayList<String>();
					currentDomain.add(boardRow.charAt(col) + "");
					csp.addVariable(row + "-" + col, currentDomain);
				}
			}
		}
		scanner.close();
		for (int row = 0; row < 9; row++) {
			ArrayList<String> variables = new ArrayList<String>();
			for (int col = 0; col < 9; col++) {
				variables.add(row + "-" + col);
			}
			csp.addAllDifferentConstraint(variables);
		}
		for (int col = 0; col < 9; col++) {
			ArrayList<String> variables = new ArrayList<String>();
			for (int row = 0; row < 9; row++) {
				variables.add(row + "-" + col);
			}
			csp.addAllDifferentConstraint(variables);
		}
		for (int boxRow = 0; boxRow < 3; boxRow++) {
			for (int boxCol = 0; boxCol < 3; boxCol++) {
				ArrayList<String> variables = new ArrayList<String>();
				for (int row = boxRow * 3; row < (boxRow + 1) * 3; row++) {
					for (int col = boxCol * 3; col < (boxCol + 1) * 3; col++) {
						variables.add(row + "-" + col);
					}
				}
				csp.addAllDifferentConstraint(variables);
			}
		}
		return csp;
	}

	/**
	 * Convert the representation of a Sudoku solution as returned from the
	 * method CSP.backtrackingSearch(), into a human readable representation.
	 */
	public static void printSudokuSolution(VariablesToDomainsMapping assignment) {
		for (int row = 0; row < 9; row++) {
			for (int col = 0; col < 9; col++) {
				System.out.print(assignment.get(row + "-" + col).get(0) + " ");
				if (col == 2 || col == 5) {
					System.out.print("| ");
				}
			}
			System.out.println();
			if (row == 2 || row == 5) {
				System.out.println("------+-------+------");
			}
		}
	}
}
