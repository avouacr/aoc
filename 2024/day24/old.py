wires, gates, wires_starting_with_z = parse_input('example2.txt')

G = nx.DiGraph()

for in1, op, in2, out in gates:
    G.add_edge(in1, out)
    G.add_edge(in2, out)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # Layout for better visualization
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10, font_weight="bold")
plt.title("Node Relationships")
plt.show()




i = 0
x = int(''.join([str(wires[f'x{j:02d}']) for j in range(i+1)]), 2)
y = int(''.join([str(wires[f'y{j:02d}']) for j in range(i+1)]), 2)
z = int(''.join([str(wires[f'z{j:02d}']) for j in range(i+2)]), 2)
x + y == z