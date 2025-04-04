#lang racket
(require picturing-programs)

; 定义重复执行函数的函数
(define (repeat k fn)
  (if (> k 0)
      (begin
        (fn)
        (repeat (- k 1) fn))))

; 定义绘制三次边并旋转的函数
(define (tri fn)
  (repeat 3 (lambda () (fn) (lt 120))))

; 定义绘制谢尔宾斯基三角形的递归函数
(define (sier d k)
  (tri (lambda () (if (= d 1) (fd k) (leg d k)))))

; 定义绘制子三角形的函数
(define (leg d k)
  (sier (- d 1) (/ k 2)))

; 主程序
(big-bang empty-scene
          (on-draw (lambda (s)
                     (penup)
                     (fd -150)
                     (pendown)
                     (sier 4 300)
                     s)))