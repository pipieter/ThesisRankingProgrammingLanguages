#include <cmath>
#include <cstdlib>
#include <iostream>
#include <vector>

using namespace std;

class TreeNode {
public:
  TreeNode *left;
  TreeNode *right;

  TreeNode(TreeNode *left, TreeNode *right) {
    this->left = left;
    this->right = right;
  }

  ~TreeNode() {
    delete left;
    delete right;
  }
};

TreeNode *build_tree(int nodes) {
  if (nodes == 0) {
    return nullptr;
  }

  int nodes_left = nodes / 2;
  int nodes_right = nodes - nodes_left - 1;

  TreeNode *left = build_tree(nodes_left);
  TreeNode *right = build_tree(nodes_right);

  return new TreeNode(left, right);
}

void count_at_depths(const TreeNode *tree, int depth, vector<int> &target) {
  if (tree == nullptr) {
    return;
  }

  target[depth] += 1;
  count_at_depths(tree->left, depth + 1, target);
  count_at_depths(tree->right, depth + 1, target);
}

int main(int argc, const char **argv) {
  int nodes = std::atoi(argv[1]);
  int depth = (int)ceil(log2((double)nodes));

  TreeNode *tree = build_tree(nodes);
  vector<int> counts(depth);

  count_at_depths(tree, 0, counts);

  for (size_t i = 0; i < depth; i++) {
    std::cout << i << " " << counts[i] << std::endl;
  }

  delete tree;

  return 0;
}