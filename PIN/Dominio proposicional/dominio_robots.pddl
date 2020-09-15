;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; ROBOTS
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain dominio_robots)
  (:requirements :strips :typing :equality)
  (:types robot taza persona lugar armario maquina brazo)
  (:predicates (at ?x - (either persona robot armario maquina) ?y - lugar)
               (on ?x - taza ?y - (either persona armario))
			   (have ?x - taza ?y - robot ?z - brazo)
			   (linked ?x - lugar ?y - lugar)
			   (allowed ?x - robot ?y - lugar)
			   (empty ?x - taza)
			   (full ?x - taza)
			   (ocupado ?x - brazo ?y - robot)
			   (libre ?x - brazo ?y - robot))

  (:action move-robot
	     :parameters (?r - robot  ?o - lugar ?d - lugar)
	     :precondition (and (at ?r ?o) (linked ?o ?d) (allowed ?r ?d))
           :effect
	               (and (not (at ?r ?o))(at ?r ?d)))

  (:action give-cup
	     :parameters (?r1 - robot ?r2 - robot ?t - taza ?l - lugar ?b1 - brazo ?b2 - brazo)
	     :precondition (and (at ?r1 ?l)(at ?r2 ?l)(have ?t ?r1 ?b1)(libre ?b2 ?r2)(ocupado ?b1 ?r1))
    	     :effect
	     (and (have ?t ?r2 ?b2) (not (have ?t ?r1 ?b1))(not (ocupado ?b1 ?r1))(ocupado ?b2 ?r2)(not (libre ?b2 ?r2))(libre ?b1 ?r1)))



  (:action fill-cup
	     :parameters (?r - robot ?m - maquina ?l - lugar ?t - taza ?b - brazo)
	     :precondition (and (at ?r ?l)(at ?m ?l)(have ?t ?r ?b)(empty ?t))
	     :effect
	     (and (not (empty ?t))(full ?t)))

  (:action serve-cup
	     :parameters (?r - robot ?p - persona ?l - lugar ?t - taza ?b - brazo)
	     :precondition (and (at ?r ?l)(at ?p ?l)(have ?t ?r ?b)(full ?t)(ocupado ?b ?r))
	     :effect
	     (and (not (have ?t ?r ?b))(on ?t ?p)(not (ocupado ?b ?r))(libre ?b ?r)))


  (:action get-cup
	     :parameters (?r - robot ?a - armario ?l - lugar ?t - taza ?b - brazo)
	     :precondition (and (at ?r ?l)(at ?a ?l)(on ?t ?a)(libre ?b ?r))
	     :effect
	     (and (not (on ?t ?a))(have ?t ?r ?b)(ocupado ?b ?r)(not (libre ?b ?r))))
)



 