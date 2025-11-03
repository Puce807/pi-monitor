
class Layout:
    cpu_label = (5, 3)
    ram_label = (130, 3)
    sent_label = (5, 18)
    recv_label = (130, 18)
    disk_label = (5, 33)

    # Disk Bar:
    disk_full_coords = [(5, 52), (245, 62)]
    disk_clear_coords = [(7, 54), (243, 60)]
    disk_fill_coords = [(7, 54), (22, 60)]

    # Graph:
    graph_full_coords = [(5, 67), (245, 116)]
    graph_clear_coords = [(7, 69), (243, 114)]

    warning_text = (125, 70)

    # Warning Icon:
    warn_out_coords = [(100, 50), (125, 12), (150, 50)]
    warn_clear_coords = [(104, 48), (125, 16), (146, 48)]
    warn_line_coords = [(124, 23), (126, 40)]
    warn_dot_coords = [(124, 43), (126, 46)]