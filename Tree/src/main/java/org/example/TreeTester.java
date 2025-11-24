package org.example;

public class TreeTester {
    public static void main(String[] args) {
        Node root = new Node(1);
        root.left = new Node(2);
        root.left.left = new Node(4);
        root.left.right = new Node(5);
        root.left.right.left = new Node(7);
        root.left.right.right = new Node(8);
        root.right = new Node(3);
        root.right.right = new Node(6);

        // Positive test case: children sum property holds
        Node posRoot = new Node(10);
        posRoot.left = new Node(8);
        posRoot.right = new Node(2);
        posRoot.left.left = new Node(3);
        posRoot.left.right = new Node(5);
        posRoot.right.right = new Node(2);
        System.out.println("Positive case (should be true): " + Node.childrenSumProperty(posRoot));

        // Negative test case: children sum property does not hold
        Node negRoot = new Node(10);
        negRoot.left = new Node(8);
        negRoot.right = new Node(2);
        negRoot.left.left = new Node(3);
        negRoot.left.right = new Node(6); // Should be 5 for property, but set to 6 to break it
        negRoot.right.right = new Node(2);
        System.out.println("Negative case (should be false): " + Node.childrenSumProperty(negRoot));

        // Node.levelOrderTraversalWithQueueAndNewLine(root);
        // Node.sizeBFS(root);
        // System.out.println("SizeDFS : " + Node.sizeDFS(root, 0));
        // System.out.println("MaxValue : " + Node.maxValue(root));
        Node.leftView(root);
    }
}
