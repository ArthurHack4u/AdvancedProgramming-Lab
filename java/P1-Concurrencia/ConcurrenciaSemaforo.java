import java.util.concurrent.Semaphore;

class RecursoCompartido {
    private final Semaphore semaforo = new Semaphore(2);

    public void usarRecurso(int idWorker) throws InterruptedException {
        System.out.println("Worker " + idWorker + " intentando acceder al recurso...");
        
        semaforo.acquire();
        
        try {
            System.out.println("--> Worker " + idWorker + " HA ACCEDIDO al recurso. Permisos restantes: " + semaforo.availablePermits());
            Thread.sleep(2000); 
        } finally {
            System.out.println("<-- Worker " + idWorker + " va a LIBERAR el recurso.");
            semaforo.release();
        }
    }
}

class Worker implements Runnable {
    private final int id;
    private final RecursoCompartido recurso;

    public Worker(int id, RecursoCompartido recurso) {
        this.id = id;
        this.recurso = recurso;
    }

    @Override
    public void run() {
        try {
            recurso.usarRecurso(id);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.err.println("Worker " + id + " fue interrumpido.");
        }
    }
}

public class ConcurrenciaSemaforo {
    public static void main(String[] args) {
        RecursoCompartido recurso = new RecursoCompartido();
        
        System.out.println("Iniciando 5 workers para un recurso con 2 slots disponibles...");

        // Creamos y arrancamos 5 hilos. Como solo hay 2 permisos, competirán por el acceso.
        for (int i = 1; i <= 5; i++) {
            Thread workerThread = new Thread(new Worker(i, recurso));
            workerThread.start();
        }
    }
}