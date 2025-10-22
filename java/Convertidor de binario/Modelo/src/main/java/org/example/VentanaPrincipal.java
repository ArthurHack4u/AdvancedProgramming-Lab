package org.example;

import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.FlowLayout;

public class VentanaPrincipal extends JFrame {

    private JTextArea jtaDatos;
    private JButton btnAbrirBinario;
    private JButton btnCsvABinario;
    private JButton btnBinACsv;
    private JLabel lblNombre;

    public VentanaPrincipal() {
        setTitle("Conversor de Archivos - Práctica 3");
        setSize(550, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JPanel panelBotones = new JPanel(new FlowLayout());

        btnAbrirBinario = new JButton("Leer Binario");
        btnCsvABinario = new JButton("Convertir CSV a Binario");
        btnBinACsv = new JButton("Convertir Binario a CSV");

        panelBotones.add(btnAbrirBinario);
        panelBotones.add(btnCsvABinario);
        panelBotones.add(btnBinACsv);
        add(panelBotones, BorderLayout.NORTH);

        jtaDatos = new JTextArea();
        jtaDatos.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(jtaDatos);
        add(scrollPane, BorderLayout.CENTER);

        lblNombre = new JLabel("Practica elaborada por Arturo Moran");
        lblNombre.setHorizontalAlignment(SwingConstants.CENTER);
        add(lblNombre, BorderLayout.SOUTH);
    }

    public JTextArea getJtaDatos() { return jtaDatos; }
    public JButton getBtnAbrirBinario() { return btnAbrirBinario; }
    public JButton getBtnCsvABinario() { return btnCsvABinario; }
    public JButton getBtnBinACsv() { return btnBinACsv; }
}