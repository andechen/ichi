//-----------------------------------------------------------------------
// Copyright 2016 Tobii AB (publ). All rights reserved.
//-----------------------------------------------------------------------

using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Tobii.Gaming;

namespace Tobii.Gaming.Examples.SimpleGazeSelection
{
	/// <summary>
	/// Changes the color of the game object's material, when the the game object 
	/// is in focus of the user's eye-gaze.
	/// </summary>
	/// <remarks>
	/// Referenced by the Target game objects in the Simple Gaze Selection example scene.
	/// </remarks>
	[RequireComponent(typeof(GazeAware))]
	[RequireComponent(typeof(MeshRenderer))]
	public class ChangeColor : MonoBehaviour
	{
		public Color selectionColor;

		private GazeAware _gazeAwareComponent;
		private MeshRenderer _meshRenderer;

		private Color _deselectionColor;
		private Color clickedColor;
		private Color _lerpColor;
		private float _fadeSpeed = 0.1f;
		private Vector3 _historicPoint;
		public float FilterSmoothingFactor = 0.15f;
		private bool _hasHistoricPoint;
		public float VisualizationDistance = 10f;
	
		/// <summary>
		/// Set the lerp color
		/// </summary>
		void Start()
		{
			_gazeAwareComponent = GetComponent<GazeAware>();
			_meshRenderer = GetComponent<MeshRenderer>();
			_lerpColor = _meshRenderer.material.color;
			_deselectionColor = Color.white;
		
		}

		/// <summary>
		/// Lerping the color
		/// </summary>
		void Update()
		{
			GazePoint gazePoint = TobiiAPI.GetGazePoint();

			if (_meshRenderer.material.color != _lerpColor)
			{
				_meshRenderer.material.color = Color.Lerp(_meshRenderer.material.color, _lerpColor, _fadeSpeed);
				
			}

			// Change the color of the cube

			//left click
			if (_gazeAwareComponent.HasGazeFocus && Input.GetMouseButtonDown(0))
			{
				_meshRenderer.material.color = Color.magenta;
				
			}
			//Click and drag
			if (_gazeAwareComponent.HasGazeFocus && Input.GetMouseButton(0) && gazePoint.IsRecent()){
				print("Gaze point on Screen (X,Y): " + gazePoint.Viewport.x + ", " + gazePoint.Viewport.y);
			
				Vector3 gazePointInWorld = ProjectToPlaneInWorld(gazePoint);
				transform.position = Smoothify(gazePointInWorld);
			}

			//left click
			else if (_gazeAwareComponent.HasGazeFocus && Input.GetMouseButtonDown(1))
			{
				_meshRenderer.material.color = Color.black;
			}
			else if (_gazeAwareComponent.HasGazeFocus)
			{
				SetLerpColor(selectionColor);
			}
			else
			{
				SetLerpColor(_deselectionColor);
			}




		}

		/// <summary>
		/// Update the color, which should used for the lerping
		/// </summary>
		/// <param name="lerpColor"></param>
		public void SetLerpColor(Color lerpColor)
		{
			this._lerpColor = lerpColor;
		}

		private Vector3 ProjectToPlaneInWorld(GazePoint gazePoint)
		{
			Vector3 gazeOnScreen = gazePoint.Screen;
			gazeOnScreen += (transform.forward * 6);
			return Camera.main.ScreenToWorldPoint(gazeOnScreen);
		}

		private Vector3 Smoothify(Vector3 point)
		{
			if (!_hasHistoricPoint)
			{
				_historicPoint = point;
				_hasHistoricPoint = true;
			}

			var smoothedPoint = new Vector3(
				point.x * (1.0f - FilterSmoothingFactor) + _historicPoint.x * FilterSmoothingFactor,
				point.y * (1.0f - FilterSmoothingFactor) + _historicPoint.y * FilterSmoothingFactor,
				point.z * (1.0f - FilterSmoothingFactor) + _historicPoint.z * FilterSmoothingFactor);
			

			_historicPoint = smoothedPoint;

			return smoothedPoint;
		}
	}
}
