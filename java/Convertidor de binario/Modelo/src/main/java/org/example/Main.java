import org.example.Controlador;
import org.example.GestorBinario;
import org.example.GestorTexto;
import org.example.VentanaPrincipal;
import javax.swing.SwingUtilities;

public class Main {

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {

                GestorTexto gestorTexto = new GestorTexto();
                GestorBinario gestorBinario = new GestorBinario();

                VentanaPrincipal vista = new VentanaPrincipal();

                new Controlador(vista, gestorTexto, gestorBinario);

                vista.setVisible(true);
            }
        });
    }
}