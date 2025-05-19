/*Feito por IA
Prompt: Como fica o código no include?*/
// include/data_structures.hpp
// Header-only implementações em C++17 de cinco estruturas de dados
#pragma once
#include <functional>
#include <vector>
#include <random>
#include <limits>
#include <optional>

// 1. Lista Encadeada Simples
#ifndef LINKED_LIST_H
#define LINKED_LIST_H

template<typename T>
class LinkedList {
public:
    struct Node { T data; Node* next; Node(const T& v): data(v), next(nullptr) {} };
    LinkedList(): head(nullptr), tail(nullptr), sz(0) {}
    ~LinkedList() { clear(); }

    void push_back(const T& v) {
        Node* node = new Node(v);
        if (!head) head = tail = node;
        else { tail->next = node; tail = node; }
        ++sz;
    }

    bool remove(const T& v) {
        Node* cur = head; Node* prev = nullptr;
        while (cur) {
            if (cur->data == v) {
                Node* del = cur;
                if (prev) prev->next = cur->next;
                else head = cur->next;
                if (cur == tail) tail = prev;
                cur = cur->next;
                delete del; --sz;
                return true;
            }
            prev = cur;
            cur = cur->next;
        }
        return false;
    }

    Node* find(const T& v) const {
        for (Node* cur = head; cur; cur = cur->next)
            if (cur->data == v) return cur;
        return nullptr;
    }

    size_t size() const { return sz; }

    void clear() {
        Node* cur = head;
        while (cur) {
            Node* nxt = cur->next;
            delete cur;
            cur = nxt;
        }
        head = tail = nullptr;
        sz = 0;
    }

    // Para iterador simples
    Node* begin() const { return head; }
    Node* end() const { return nullptr; }

private:
    Node* head;
    Node* tail;
    size_t sz;
};

#endif // LINKED_LIST_H


// 2. Árvore Binária de Busca (BST)
#ifndef BST_H
#define BST_H

template<typename Key, typename Value>
class BST {
public:
    struct Node { Key key; Value val; Node* left; Node* right;
        Node(const Key& k, const Value& v): key(k), val(v), left(nullptr), right(nullptr) {}
    };
    BST(): root(nullptr) {}
    ~BST() { clear(root); }

    void insert(const Key& k, const Value& v) { root = insert_rec(root, k, v); }
    bool remove(const Key& k) { bool rem = false; root = remove_rec(root, k, rem); return rem; }
    Value* find(const Key& k) const { Node* n = find_rec(root, k); return n ? &n->val : nullptr; }

private:
    Node* root;

    Node* insert_rec(Node* t, const Key& k, const Value& v) {
        if (!t) return new Node(k, v);
        if (k < t->key) t->left = insert_rec(t->left, k, v);
        else if (k > t->key) t->right = insert_rec(t->right, k, v);
        else t->val = v;
        return t;
    }

    Node* remove_rec(Node* t, const Key& k, bool& rem) {
        if (!t) return nullptr;
        if (k < t->key) t->left = remove_rec(t->left, k, rem);
        else if (k > t->key) t->right = remove_rec(t->right, k, rem);
        else {
            rem = true;
            if (!t->left) { Node* r = t->right; delete t; return r; }
            if (!t->right) { Node* l = t->left; delete t; return l; }
            Node* succ = t->right;
            while (succ->left) succ = succ->left;
            t->key = succ->key;
            t->val = succ->val;
            t->right = remove_rec(t->right, succ->key, rem);
        }
        return t;
    }

    Node* find_rec(Node* t, const Key& k) const {
        if (!t) return nullptr;
        if (k < t->key) return find_rec(t->left, k);
        if (k > t->key) return find_rec(t->right, k);
        return t;
    }

    void clear(Node* t) {
        if (!t) return;
        clear(t->left);
        clear(t->right);
        delete t;
    }
};

#endif // BST_H


// 3. Hash Table (endereçamento aberto, linear probing)
#ifndef HASH_TABLE_H
#define HASH_TABLE_H

template<typename Key, typename Value>
class HashTable {
public:
    HashTable(size_t cap = 1024): capacity(cap), size_(0) {
        keys.resize(capacity);
        vals.resize(capacity);
        occupied.assign(capacity, false);
    }

    bool insert(const Key& k, const Value& v) {
        if (size_ >= capacity * 0.7) rehash(capacity * 2);
        size_t idx = hasher(k) % capacity;
        while (occupied[idx]) {
            if (keys[idx] == k) { vals[idx] = v; return true; }
            idx = (idx + 1) % capacity;
        }
        keys[idx] = k;
        vals[idx] = v;
        occupied[idx] = true;
        ++size_;
        return true;
    }

    std::optional<Value> find(const Key& k) const {
        size_t idx = hasher(k) % capacity;
        size_t start = idx;
        do {
            if (!occupied[idx]) return std::nullopt;
            if (keys[idx] == k) return vals[idx];
            idx = (idx + 1) % capacity;
        } while (idx != start);
        return std::nullopt;
    }

private:
    size_t capacity;
    size_t size_;
    std::vector<Key> keys;
    std::vector<Value> vals;
    std::vector<bool> occupied;
    std::hash<Key> hasher;

    void rehash(size_t new_cap) {
        std::vector<Key> old_k = keys;
        std::vector<Value> old_v = vals;
        std::vector<bool> old_occ = occupied;
        capacity = new_cap;
        size_ = 0;
        keys.assign(capacity, Key());
        vals.assign(capacity, Value());
        occupied.assign(capacity, false);
        for (size_t i = 0; i < old_k.size(); ++i) {
            if (old_occ[i]) insert(old_k[i], old_v[i]);
        }
    }
};

#endif // HASH_TABLE_H


// 4. Árvore AVL
#ifndef AVL_TREE_H
#define AVL_TREE_H

template<typename Key, typename Value>
class AVLTree {
public:
    struct Node { Key key; Value val; Node* left; Node* right; int h;
        Node(const Key& k, const Value& v): key(k), val(v), left(nullptr), right(nullptr), h(1) {}
    };
    AVLTree(): root(nullptr) {}
    ~AVLTree() { clear(root); }

    void insert(const Key& k, const Value& v) { root = insert_rec(root, k, v); }
    bool remove(const Key& k) { bool rem = false; root = remove_rec(root, k, rem); return rem; }
    Value* find(const Key& k) const { Node* n = find_rec(root, k); return n ? &n->val : nullptr; }

private:
    Node* root;

    int height(Node* n) const { return n ? n->h : 0; }
    int balance(Node* n) const { return height(n->left) - height(n->right); }
    void update_height(Node* n) { n->h = 1 + std::max(height(n->left), height(n->right)); }

    Node* right_rotate(Node* y) {
        Node* x = y->left;
        y->left = x->right;
        x->right = y;
        update_height(y);
        update_height(x);
        return x;
    }

    Node* left_rotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        y->left = x;
        update_height(x);
        update_height(y);
        return y;
    }

    Node* insert_rec(Node* n, const Key& k, const Value& v) {
        if (!n) return new Node(k, v);
        if (k < n->key) n->left = insert_rec(n->left, k, v);
        else if (k > n->key) n->right = insert_rec(n->right, k, v);
        else { n->val = v; return n; }
        update_height(n);
        int bal = balance(n);
        if (bal > 1 && k < n->left->key) return right_rotate(n);
        if (bal < -1 && k > n->right->key) return left_rotate(n);
        if (bal > 1 && k > n->left->key) { n->left = left_rotate(n->left); return right_rotate(n); }
        if (bal < -1 && k < n->right->key) { n->right = right_rotate(n->right); return left_rotate(n); }
        return n;
    }

    Node* remove_rec(Node* n, const Key& k, bool& rem) {
        if (!n) return nullptr;
        if (k < n->key) n->left = remove_rec(n->left, k, rem);
        else if (k > n->key) n->right = remove_rec(n->right, k, rem);
        else {
            rem = true;
            if (!n->left || !n->right) {
                Node* tmp = n->left ? n->left : n->right;
                delete n;
                return tmp;
            }
            Node* succ = n->right;
            while (succ->left) succ = succ->left;
            n->key = succ->key;
            n->val = succ->val;
            n->right = remove_rec(n->right, succ->key, rem);
        }
        update_height(n);
        int bal = balance(n);
        if (bal > 1 && balance(n->left) >= 0) return right_rotate(n);
        if (bal > 1 && balance(n->left) < 0) { n->left = left_rotate(n->left); return right_rotate(n); }
        if (bal < -1 && balance(n->right) <= 0) return left_rotate(n);
        if (bal < -1 && balance(n->right) > 0) { n->right = right_rotate(n->right); return left_rotate(n); }
        return n;
    }

    Node* find_rec(Node* n, const Key& k) const {
        if (!n) return nullptr;
        if (k < n->key) return find_rec(n->left, k);
        if (k > n->key) return find_rec(n->right, k);
        return n;
    }

    void clear(Node* n) { if (!n) return; clear(n->left); clear(n->right); delete n; }
};

#endif // AVL_TREE_H


// 5. Skip List
#ifndef SKIP_LIST_H
#define SKIP_LIST_H

template<typename Key, typename Value>
class SkipList {
    struct Node { Key key; Value val; std::vector<Node*> next;
        Node(const Key& k, const Value& v, int lvl): key(k), val(v), next(lvl,nullptr) {}
    };
public:
    SkipList(int maxLevel = 16, double prob = 0.5)
      : MAX_LEVEL(maxLevel), level(1), dist(prob), rd(), gen(rd()) {
        head = new Node(Key(), Value(), MAX_LEVEL);
    }
    ~SkipList() { clear(); }

    void insert(const Key& k, const Value& v) {
        std::vector<Node*> update(MAX_LEVEL);
        Node* x = head;
        for (int i = level-1; i >= 0; --i) {
            while (x->next[i] && x->next[i]->key < k) x = x->next[i];
            update[i] = x;
        }
        x = x->next[0];
        if (x && x->key == k) { x->val = v; return; }
        int lvl = random_level();
        if (lvl > level) {
            for (int i = level; i < lvl; ++i) update[i] = head;
            level = lvl;
        }
        Node* n = new Node(k, v, lvl);
        for (int i = 0; i < lvl; ++i) {
            n->next[i] = update[i]->next[i];
            update[i]->next[i] = n;
        }
    }

    bool remove(const Key& k) {
        std::vector<Node*> update(MAX_LEVEL);
        Node* x = head;
        for (int i = level-1; i >= 0; --i) {
            while (x->next[i] && x->next[i]->key < k) x = x->next[i];
            update[i] = x;
        }
        x = x->next[0];
        if (!x || x->key != k) return false;
        for (int i = 0; i < level; ++i) {
            if (update[i]->next[i] != x) break;
            update[i]->next[i] = x->next[i];
        }
        delete x;
        while (level > 1 && !head->next[level-1]) --level;
        return true;
    }

    Value* find(const Key& k) const {
        Node* x = head;
        for (int i = level-1; i >= 0; --i) {
            while (x->next[i] && x->next[i]->key < k) x = x->next[i];
        }
        x = x->next[0];
        return (x && x->key == k) ? &x->val : nullptr;
    }

private:
    Node* head;
    int level;
    const int MAX_LEVEL;
    double dist;
    std::random_device rd;
    std::mt19937 gen;

    int random_level() {
        int lvl = 1;
        std::bernoulli_distribution d(dist);
        while (d(gen) && lvl < MAX_LEVEL) ++lvl;
        return lvl;
    }

    void clear() {
        Node* cur = head->next[0];
        while (cur) {
            Node* tmp = cur->next[0];
            delete cur;
            cur = tmp;
        }
        delete head;
    }
};

#endif // SKIP_LIST_H
