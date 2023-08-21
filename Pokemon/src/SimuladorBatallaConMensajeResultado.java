import javax.sound.sampled.*;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.IOException;
import javax.imageio.ImageIO;

public class SimuladorBatallaConMensajeResultado {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new MarcoBatalla();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setVisible(true);
        });
    }
}

class MarcoBatalla extends JFrame {
    private Pokemon pokemonJugador;
    private Pokemon pokemonEnemigo;
    private JTextArea areaTextoBatalla;
    private JLabel imagenPokemonJugador;
    private JLabel imagenNueva;
    private JLabel imagenPokemonEnemigo;
    private JLabel mensajeResultado;

    public MarcoBatalla() {
        setTitle("Simulador de Batalla Pokémon");
        setSize(1000, 400);
        setLayout(new BorderLayout());

        areaTextoBatalla = new JTextArea();
        areaTextoBatalla.setEditable(false);
        add(new JScrollPane(areaTextoBatalla), BorderLayout.CENTER);

        pokemonJugador = new Pokemon("Pikachu", 100);
        pokemonEnemigo = new Pokemon("Charmander", 110);

        imagenPokemonJugador = new JLabel();
        imagenNueva = new JLabel(); // Espacio para la nueva imagen
        imagenPokemonEnemigo = new JLabel();

        mensajeResultado = new JLabel();
        mensajeResultado.setHorizontalAlignment(JLabel.CENTER);
        add(mensajeResultado, BorderLayout.NORTH);

        cargarImagenes();

        JPanel panelImagenes = new JPanel();
        panelImagenes.setLayout(new FlowLayout());
        panelImagenes.add(imagenPokemonJugador);
        panelImagenes.add(imagenNueva);
        panelImagenes.add(imagenPokemonEnemigo);

        add(panelImagenes, BorderLayout.SOUTH);

        iniciarBatalla();
    }

    private void cargarImagenes() {
        try {
            BufferedImage imagenPikachu = ImageIO.read(SimuladorBatallaConMensajeResultado.class.getResourceAsStream("imagenes/pikachu.png"));
            BufferedImage imagenCharmander = ImageIO.read(SimuladorBatallaConMensajeResultado.class.getResourceAsStream("imagenes/charmander.png"));
            BufferedImage imagenNuevaImagen = ImageIO.read(SimuladorBatallaConMensajeResultado.class.getResourceAsStream("imagenes/vs.png")); // Cambia "nueva_imagen.png" por el nombre de tu imagen

            ImageIcon iconoPikachu = new ImageIcon(imagenPikachu.getScaledInstance(100, 100, Image.SCALE_SMOOTH));
            ImageIcon iconoCharmander = new ImageIcon(imagenCharmander.getScaledInstance(100, 100, Image.SCALE_SMOOTH));
            ImageIcon iconoNuevaImagen = new ImageIcon(imagenNuevaImagen.getScaledInstance(100, 100, Image.SCALE_SMOOTH));

            imagenPokemonJugador.setIcon(iconoPikachu);
            imagenNueva.setIcon(iconoNuevaImagen);
            imagenPokemonEnemigo.setIcon(iconoCharmander);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void iniciarBatalla() {
        Thread hiloAudio = new Thread(() -> reproducirAudio());
        Thread hiloBatalla = new Thread(() -> bucleBatalla());

        hiloAudio.start();
        hiloBatalla.start();
    }

    private void reproducirAudio() {
        try {
            AudioFormat formato = new AudioFormat(44100, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, formato);
            SourceDataLine linea = (SourceDataLine) AudioSystem.getLine(info);

            linea.open(formato);
            linea.start();

            int tamanoBuffer = 4096;
            byte[] buffer = new byte[tamanoBuffer];

            AudioInputStream flujoAudio = AudioSystem.getAudioInputStream(SimuladorBatallaConMensajeResultado.class.getResourceAsStream("audio/pokemon-battle.wav"));
            int bytesLeidos;
            while ((bytesLeidos = flujoAudio.read(buffer, 0, buffer.length)) != -1) {
                linea.write(buffer, 0, bytesLeidos);
            }

            linea.drain();
            linea.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void bucleBatalla() {
        while (pokemonJugador.getHP() > 0 && pokemonEnemigo.getHP() > 0) {
            pokemonJugador.atacar(pokemonEnemigo);
            pokemonEnemigo.atacar(pokemonJugador);
            actualizarTextoBatalla(pokemonJugador, pokemonEnemigo);

            try {
                Thread.sleep(1000); // Pausa para mostrar el mensaje antes de la siguiente iteración
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        mostrarResultado();
    }

    private void mostrarResultado() {
        if (pokemonJugador.getHP() <= 0) {
            mensajeResultado.setText("¡Charmander ha ganado!");
        } else {
            mensajeResultado.setText("¡Pikachu ha ganado!");
        }
    }

    private void actualizarTextoBatalla(Pokemon jugador, Pokemon enemigo) {
        String estadoBatalla = jugador.getNombre() + " HP: " + jugador.getHP() +
                "\n" + enemigo.getNombre() + " HP: " + enemigo.getHP();
        areaTextoBatalla.append(estadoBatalla + "\n");
    }
}

class Pokemon {
    private String nombre;
    private int hp;

    public Pokemon(String nombre, int hp) {
        this.nombre = nombre;
        this.hp = hp;
    }

    public String getNombre() {
        return nombre;
    }

    public int getHP() {
        return hp;
    }

    public void atacar(Pokemon objetivo) {
        int danio = 10;
        objetivo.hp -= danio;
        System.out.println(nombre + " ataca a " + objetivo.nombre + " y causa " + danio +  " de daño.");
    }
}
