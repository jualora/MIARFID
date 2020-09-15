;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ROBOTS
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain dominio_robots)
  (:requirements :strips :typing :equality :durative-actions :fluents)
  (:types robot taza persona lugar armario maquina brazo)
  (:predicates (at ?x - (either persona robot armario maquina) ?y - lugar)
               (on ?x - taza ?y - (either persona robot armario))
			   (have ?x - taza ?y - robot ?z - brazo)
			   (linked ?x - lugar ?y - lugar)
			   (allowed ?x - robot ?y - lugar)
			   (empty ?x - taza)
			   (full ?x - taza)
			   (ocupado ?x - brazo ?y - robot)
			   (libre ?x - brazo ?y - robot))

  (:functions 
	  (velocidad ?r - robot)
	  (distancia ?o - lugar ?d - lugar)
	  (peso ?t - taza)
  )
  (:durative-action move-robot
	     :parameters (?r - robot  ?o - lugar ?d - lugar)
	     :duration (= ?duration (/ (distancia ?o ?d) (velocidad ?r)))
		 :condition (and (at start (at ?r ?o)) (over all (at ?r ?o)) (over all (linked ?o ?d)) (over all (allowed ?r ?d)))
         :effect
	            (and 
				   	(at end (not (at ?r ?o)))
					(at end (at ?r ?d))
				)
	)

  (:durative-action give-cup
	     :parameters (?r1 - robot ?r2 - robot ?t - taza ?l - lugar ?b1 - brazo ?b2 - brazo)
	     :duration (= ?duration (peso ?t))
		 :condition (and (at start (at ?r1 ?l)) (over all (at ?r1 ?l)) (at start (at ?r2 ?l)) (over all(at ?r2 ?l)) (at start (have ?t ?r1 ?b1)) (over all (have ?t ?r1 ?b1)) (at start (libre ?b2 ?r2)) (over all (libre ?b2 ?r2)) (at start (ocupado ?b1 ?r1)) (over all (ocupado ?b1 ?r1)))
    	 :effect
	     		(and 
					(at end (have ?t ?r2 ?b2)) 
					(at end (not (have ?t ?r1 ?b1)))
					(at end (not (ocupado ?b1 ?r1)))
					(at end (ocupado ?b2 ?r2))
					(at end (not (libre ?b2 ?r2)))
					(at end (libre ?b1 ?r1))
					(at end (at ?r1 ?l))
					(at end (at ?r2 ?l))
				)
	)

  (:durative-action fill-cup
	     :parameters (?r - robot ?m - maquina ?l - lugar ?t - taza ?b - brazo)
	     :duration (= ?duration 2)
		 :condition (and (at start (at ?r ?l)) (over all (at ?r ?l))(over all (at ?m ?l))(at start (have ?t ?r ?b))(over all (have ?t ?r ?b))(at start (empty ?t))(over all (empty ?t)))
	     :effect
	     		(and 
				 	(at end (not (empty ?t)))
					(at end (full ?t))
					(at end (increase (peso ?t) (+ (peso ?t) 1)))
					(at end (at ?r ?l))
					(at end (have ?t ?r ?b))
				)
	)

  (:durative-action serve-cup
	     :parameters (?r - robot ?p - persona ?l - lugar ?t - taza ?b - brazo)
	     :duration (= ?duration (peso ?t))
		 :condition (and (at start (at ?r ?l))(over all (at ?r ?l)) (at start (at ?p ?l)) (over all (at ?p ?l)) (at start (have ?t ?r ?b)) (over all (have ?t ?r ?b)) (at start (full ?t)) (over all (full ?t)) (at start (ocupado ?b ?r)) (over all (ocupado ?b ?r)))
	     :effect
	     		(and 
					(at end (not (have ?t ?r ?b)))
					(at end (on ?t ?p))
					(at end (not (ocupado ?b ?r)))
					(at end (libre ?b ?r))
					(at end (at ?r ?l))
					(at end (at ?p ?l))
				)
	)


  (:durative-action get-cup
	     :parameters (?r - robot ?a - armario ?l - lugar ?t - taza ?b - brazo)
	     :duration (= ?duration 2)
		 :condition (and (at start (at ?r ?l)) (over all (at ?r ?l)) (over all (at ?a ?l)) (at start (on ?t ?a)) (over all (on ?t ?a)) (at start (libre ?b ?r)) (over all (libre ?b ?r)))
	     :effect
	     		(and 
					(at end (not (on ?t ?a)))
					(at end (have ?t ?r ?b))
					(at end (ocupado ?b ?r))
					(at end (not (libre ?b ?r)))
					(at end (at ?r ?l))
				)
	)
)



 