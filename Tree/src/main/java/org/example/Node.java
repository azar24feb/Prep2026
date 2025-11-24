package org.example;

import javax.sound.midi.Soundbank;
import java.util.LinkedList;
import java.util.Queue;

public class Node {

    public int key;
    public Node left;
    public Node right;

    public Node(int key) {
        this.key = key;
    }

    public static void inOrder(Node root) {
        if (root == null) return;
        inOrder(root.left);
        System.out.println(root.key);
        inOrder(root.right);
    }

    public static void preOrder(Node root) {
        if (root == null) return;
        System.out.println(root.key);
        preOrder(root.left);
        preOrder(root.right);
    }

    public static void postOrder(Node root) {
        if (root == null) return;
        postOrder(root.left);
        postOrder(root.right);
        System.out.println(root.key);
    }

    public static int height(Node root) {
        if (root == null) return 0;
        return Integer.max(height(root.left), height(root.right)) + 1;
    }

    public static void printK(Node root, int k) {
        if (root == null) return;
        if (k == 0) System.out.println(root.key);
        printK(root.left, k - 1);
        printK(root.right, k - 1);
    }

    public static void levelOrderTraversalWithPrintK(Node root) {
        int height = height(root);
        for (int i = 0; i < height; i++) {
            printK(root, i);
        }
    }

    /**
     * Level order traversal or Breadth First Search with Queue
     */
    public static void levelOrderTraversalWithQueue(Node root) {
        if (root == null) return;
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            Node curr = q.poll();
            System.out.println(curr.key);
            if (curr.left != null) q.add(curr.left);
            if (curr.right != null) q.add(curr.right);
        }
    }

    /**
     * Level order traversal or Breadth First Search with Queue  and NewLine
     */
    public static void levelOrderTraversalWithQueueAndNewLine(Node root) {
        if (root == null) return;
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                Node curr = q.poll();
                System.out.print(curr.key + " ");
                if (curr.left != null) q.add(curr.left);
                if (curr.right != null) q.add(curr.right);
            }
            System.out.println();
        }
    }

    /**
     * Size of Tree using BFS
     */
    public static void sizeBFS(Node root) {
        if (root == null) return;
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        int size = 0;
        while (!q.isEmpty()) {
            Node curr = q.poll();
            size++;
            if (curr.left != null) q.add(curr.left);
            if (curr.right != null) q.add(curr.right);

        }
        System.out.println("SizeBFS : " + size);
    }

    /**
     * Size of Tree using DFS
     */
    public static int sizeDFS(Node root, int size) {
        if (root == null) return 0;
        return 1 + sizeDFS(root.left, size) + sizeDFS(root.right, size);
    }

    /**
     * Max value in a BT
     */
    public static int maxValue(Node root) {
        if (root == null) return 0;
        if (root.left == null && root.right == null) return root.key;
        return Integer.max(maxValue(root.left), maxValue(root.right));
    }

    /**
     * Print left view
     */
    public static void leftView(Node root) {
        if (root == null) return;
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            int size = q.size();
            for (int i = 0; i < size; i++) {
                Node curr = q.poll();
                if (curr.left != null) q.add(curr.left);
                if (curr.right != null) q.add(curr.right);
                if (i == 0)
                    System.out.print(curr.key + " ");
            }
            System.out.println();
        }
    }

    /**
     * Print left view with Recursion
     */
    public static void leftViewRecursive(Node root, int level) {
        if (root == null) return;

    }

    /**
     * Children Sum Property
     */
    public static boolean childrenSumProperty(Node root){
        if (root == null) return true;
        if (root.left == null && root.right == null) return true;
        int left = root.left == null ? 0 : root.left.key;
        int right = root.right == null ? 0 : root.right.key;
        if (root.key == left + right)
            return (true && childrenSumProperty(root.left) && childrenSumProperty(root.right));
        return false;
    }

}
