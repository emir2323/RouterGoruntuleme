import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import numpy as np

# Boş bir ağ oluşturalım
G = nx.Graph()

# Routerları düğüm olarak ekleme
num_routers = 15
faculty_names = [
    "Teknoloji Fakültesi",
    "Mimarlık Fakültesi",
    "Yabancı Diller Fakültesi",
    "Eğitim Fakültesi",
    "Sağlık Bilimleri Fakültesi",
    "Su Ürünleri Fakültesi",
    "BESYO",
    "Bilgisayar Mühendisliği",
    "Yazılım Mühendisliği Fakültesi",
    "Veterinerlik Fakültesi",
    "Tıp Fakültesi",
    "Diş Hekimliği Fakültesi",
    "İlahiyat Fakültesi",
    "Adli Bilişim Fakültesi",
    "Eczacılık Fakültesi"
]

for i in range(num_routers):
    G.add_node(i, faculty=faculty_names[i])

# Rastgele bağlantılar ekleme
edges = [
    (0, 1, 4), (1, 2, 2), (2, 3, 5), (3, 4, 2), 
    (4, 5, 3), (5, 6, 1), (6, 7, 2), (7, 8, 1), 
    (8, 9, 5), (9, 10, 1), (10, 11, 4), (11, 12, 3), 
    (12, 13, 2), (13, 14, 3), (14, 0, 6)
]
G.add_weighted_edges_from(edges)

# Manuel olarak düğüm pozisyonları belirleme
pos = {
    0: (38.682, 39.198),  # teknoloji
    1: (38.673, 39.196),  # mimarlık
    2: (38.676, 39.190),  # yabancı diller
    3: (38.681, 39.195),  # eğitim
    4: (38.684, 39.194),  # sağlık bilimleri
    5: (38.685, 39.194),  # su ürünleri
    6: (38.683, 39.194),  # BESYO
    7: (38.674, 39.190),  # bilgisayar müh
    8: (38.676, 39.193),  # yazılım müh fak
    9: (38.680, 39.201),  # veteriner
    10: (38.680, 39.205),  # tıp
    11: (38.681, 39.205),  # diş
    12: (38.680, 39.189),  # ilahiyat
    13: (38.681, 39.199),  # adli bilişim
    14: (38.679, 39.189)   # eczacılık
}

# Bilgisayar simgesi ekleme fonksiyonu
def add_computer_node(ax, pos, node, faculty):
    image_path = "desktop.png"  # İndirdiğiniz bilgisayar simgesinin yolunu buraya ekleyin
    image = plt.imread(image_path)
    im = OffsetImage(image, zoom=0.05)
    im.image.axes = ax
    ab = AnnotationBbox(im, pos, xycoords='data', frameon=False)
    ax.add_artist(ab)
    G.nodes[node]['image'] = ab
    ax.text(pos[0], pos[1] + 0.0005, faculty, color='black', ha='center', va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))  # Fakülte adını ekleme

# Ağı görselleştirme
fig, ax = plt.subplots(figsize=(12, 10))

# Düğümleri ve kenarları çizme
nx.draw(G, pos, with_labels=False, node_size=1, ax=ax, edge_color='#d3d3d3', width=2.0, style='solid')  # Çizgileri kesiksiz yapma

# Düğümler üzerinde etiketleri gösterme
labels = nx.get_node_attributes(G, 'faculty')
nx.draw_networkx_labels(G, pos, labels=labels, font_size=1, font_color='black')

# Düğümleri tıklanabilir hale getirme
nodes = nx.draw_networkx_nodes(G, pos, node_size=300, ax=ax, node_color='blue', alpha=0.5)
nodes.set_picker(True)

# Kullanıcı tarafından seçilecek fakülteler
selected_faculties = []

# Bilgisayar simgelerini tutacak dictionary
computer_nodes = {}

def init():
    for i in range(num_routers):
        computer_nodes[i] = None
    return ax,

def update(frame):
    node = frame
    if computer_nodes[node] is None:
        image_path = "desktop.png"  # İndirdiğiniz bilgisayar simgesinin yolunu buraya ekleyin
        image = plt.imread(image_path)
        im = OffsetImage(image, zoom=0.05)
        im.image.axes = ax
        ab = AnnotationBbox(im, pos[node], xycoords='data', frameon=False)
        ax.add_artist(ab)
        computer_nodes[node] = {'image': ab, 'pos': pos[node], 'faculty': G.nodes[node]['faculty']}
        ax.text(pos[node][0], pos[node][1] + 0.0005, G.nodes[node]['faculty'], color='black', ha='center', va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))  # Fakülte adını ekleme
    return ax,

ani = FuncAnimation(fig, update, frames=np.arange(num_routers), init_func=init, interval=750)  # Her 0.75 saniyede bir güncelleme yap

# Fakülteler arası en kısa yol
def show_shortest_path(event):
    global selected_faculties
    if len(selected_faculties) == 2:
        ax.clear()
        nx.draw(G, pos, with_labels=False, node_size=1, ax=ax, edge_color='#d3d3d3', width=2.0, style='solid')
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black', font_weight='bold')
        nodes = nx.draw_networkx_nodes(G, pos, node_size=300, ax=ax, node_color='blue', alpha=0.5)
        nodes.set_picker(True)
        index1 = faculty_names.index(selected_faculties[0])
        index2 = faculty_names.index(selected_faculties[1])
        
        # Belman-Ford algoritması ile en kısa yolu bulma
        try:
            shortest_path = nx.bellman_ford_path(G, index1, index2, weight='weight')  # Belman-Ford algoritması burada kullanılıyor
            edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3.0, ax=ax)
            for node in shortest_path:
                add_computer_node(ax, pos[node], node, G.nodes[node]['faculty'])
        except nx.NetworkXNoPath:
            print("Belman-Ford: Seçilen fakülteler arasında bir yol bulunamadı.")
        
        plt.axis('off')
        plt.draw()
        fig.canvas.draw_idle()  # Butonların işlevselliğini sağlamak için

def reset_selection(event):
    global selected_faculties
    selected_faculties = []
    ax.clear()
    nx.draw(G, pos, with_labels=False, node_size=1, ax=ax, edge_color='#d3d3d3', width=2.0, style='solid')
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black', font_weight='bold')
    nodes = nx.draw_networkx_nodes(G, pos, node_size=300, ax=ax, node_color='blue', alpha=0.5)
    nodes.set_picker(True)
    for i in range(num_routers):
        add_computer_node(ax, pos[i], i, G.nodes[i]['faculty'])
    plt.axis('off')
    plt.draw()

def onpick(event):
    global selected_faculties
    node_ind = event.ind[0]
    faculty = faculty_names[node_ind]
    if len(selected_faculties) < 2:
        selected_faculties.append(faculty)
        print(f"{faculty} seçildi.")
        if len(selected_faculties) == 2:
            button_show.on_clicked(show_shortest_path)

# Butonlar için alt subplot oluşturma
button_ax_show = plt.axes([0.7, 0.05, 0.1, 0.075])  # sol, alt, genişlik, yükseklik
button_show = Button(button_ax_show, 'Göster', color='blue', hovercolor='red')

button_ax_reset = plt.axes([0.8, 0.05, 0.1, 0.075])  # sol, alt, genişlik, yükseklik
button_reset = Button(button_ax_reset, 'Sıfırla', color='blue', hovercolor='red')

# Butonlara tıklama olaylarını bağlama
button_show.on_clicked(show_shortest_path)
button_reset.on_clicked(reset_selection)

# Tıklama olaylarını dinleme
fig.canvas.mpl_connect('pick_event', onpick)

plt.axis('off')
plt.tight_layout()
plt.show()
