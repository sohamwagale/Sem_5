import java.rmi.*;
import java.rmi.registry.*;

public class Server {
    public static void main(String args[]) {
        try {
            HelloImpl obj = new HelloImpl();
            LocateRegistry.createRegistry(1099); // Starts RMI registry in code
            Naming.rebind("rmi://10.1.2.186/HelloService", obj); // Use actual IP here
            System.out.println("Server is ready.");
        } catch (Exception e) {
            System.out.println("Server error: " + e);
        }
    }
}
