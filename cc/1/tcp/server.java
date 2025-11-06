//TCP Server
import java.util.*;
import java.net.*;
import java.io.*;

class tcpserver {

    public static int fact(int n){
        if(n<=1) return n;
        return n*fact(n-1);
    }

    public static void main(String args[]) {
        try {
            ServerSocket s1 = new ServerSocket(1520);
            Socket s2 = s1.accept();

            DataInputStream dis;
            DataOutputStream dos;

            InputStream is;
            OutputStream os;

            is = s2.getInputStream();
            os = s2.getOutputStream();

            dis = new DataInputStream(is);
            dos = new DataOutputStream(os);

            Scanner sc = new Scanner(System.in);

            String str;
            do {

                str = dis.readUTF();
                System.out.println("Data Received: ");
                System.out.println(str);
                System.out.println("Data sent: ");
                String fac = Integer.toString(fact(Integer.parseInt(str)));
                System.out.println(fac);
                dos.writeUTF(fac);
            } while (!str.equals("STOP"));
            sc.close();
            s1.close();
        } 
        catch (Exception e) {
        }
    }
}
